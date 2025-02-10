package wood.mike.client;

import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import io.grpc.stub.StreamObserver;
import wood.mike.*;

import java.util.Iterator;
import java.util.Scanner;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.TimeUnit;
import java.util.stream.Stream;

public class SeClient {

    private static final String HOST = "localhost";
    private static final int PORT = 50052;

    private final SecretEscapesGrpc.SecretEscapesBlockingStub blockingStub;
    private final SecretEscapesGrpc.SecretEscapesStub nonBlockingStub;
    private final ManagedChannel channel;
    private final Scanner scanner;

    public SeClient() {
        channel = ManagedChannelBuilder.forAddress(HOST, PORT)
                .usePlaintext()
                .build();

        blockingStub = SecretEscapesGrpc.newBlockingStub(channel);
        nonBlockingStub = SecretEscapesGrpc.newStub(channel);
        scanner = new Scanner(System.in);
    }

    private void run() throws InterruptedException {
        String result = switch (getChoice()) {
            case 1 -> unaryExample();
            case 2 -> serverStreamingExample();
            case 3 -> clientStreamingExample();
            case 4 -> bidirectionalStreamingExample();
            default -> throw new IllegalStateException("Unexpected value");
        };

        System.out.println(result);
        close();
    }

    private String unaryExample() {
        var seResponse =
                blockingStub.getSeSale(
                        SeSaleRequest
                        .newBuilder()
                        .setId(1).build());
        return String.format("Server reply: %s", seResponse);
    }

    private String serverStreamingExample() {
        Iterator<SeSaleReply> seSaleReplyIterator =
                blockingStub.getAllSeSales(SeSaleRangeRequest
                        .newBuilder()
                        .setStart("2025-02-01")
                        .setEnd("2025-02-07")
                        .build());

        seSaleReplyIterator.forEachRemaining(System.out::println);
        return "Done";
    }

    private String clientStreamingExample() throws InterruptedException {
        CountDownLatch latch = new CountDownLatch(1);

        StreamObserver<BatchSeSaleReply> responseObserver = new StreamObserver<>() {
            @Override
            public void onNext(BatchSeSaleReply batchSeSaleReply) {
                batchSeSaleReply.getRepliesList().forEach(req ->
                        System.out.println("SE sale: " + req)
                );
            }

            @Override
            public void onError(Throwable t) {
                System.err.println("Error from server: " + t.getMessage());
                latch.countDown();
            }

            @Override
            public void onCompleted() {
                System.out.println("Server finished processing.");
                latch.countDown();
            }
        };

        StreamObserver<SeSaleRequest> requestObserver =
                nonBlockingStub.getBatchedSeSales(responseObserver);

        Stream.of(1,2,3,4,5).map(id ->
            SeSaleRequest.newBuilder()
                .setId(id)
                .build()
        ).forEach(requestObserver::onNext);

        requestObserver.onCompleted();

        latch.await(5, TimeUnit.SECONDS);

        return "Done";
    }

    private String bidirectionalStreamingExample() throws InterruptedException {
        // Latch to wait for the server responses before shutting down
        CountDownLatch latch = new CountDownLatch(1);

        // Handle server responses
        StreamObserver<PackageRequest> requestObserver =
                nonBlockingStub.customizePackage(new StreamObserver<PackageResponse>() {
            @Override
            public void onNext(PackageResponse response) {
                System.out.println("Received response:");
                System.out.println("Type: " + response.getSelectionType());
                System.out.println("ID: " + response.getSelectionId());
                System.out.println("Available: " + response.getAvailable());
                System.out.println("Price: $" + response.getPrice());
                System.out.println("Message: " + response.getMessage());
                System.out.println("----------------------------------");
            }

            @Override
            public void onError(Throwable t) {
                System.err.println("Error from server: " + t.getMessage());
                latch.countDown();
            }

            @Override
            public void onCompleted() {
                System.out.println("Server completed sending responses.");
                latch.countDown();
            }
        });

        PackageRequest flightRequest = PackageRequest.newBuilder()
                .setUserId("user123")
                .setSelectionType("flight")
                .setSelectionId("FL123")
                .setQuantity(1)
                .build();

        PackageRequest hotelRequest = PackageRequest.newBuilder()
                .setUserId("user123")
                .setSelectionType("hotel")
                .setSelectionId("HT456")
                .setQuantity(3)
                .build();

        PackageRequest tourRequest = PackageRequest.newBuilder()
                .setUserId("user123")
                .setSelectionType("tour")
                .setSelectionId("TR789")
                .setQuantity(2)
                .build();

        System.out.println("Sending package customization requests...");
        requestObserver.onNext(flightRequest);
        requestObserver.onNext(hotelRequest);
        requestObserver.onNext(tourRequest);

        // Mark the end of requests
        requestObserver.onCompleted();

        // Wait until server finishes sending responses
        latch.await(5, TimeUnit.SECONDS);

        return "Done";
    }

    private void close() {
        scanner.close();
        channel.shutdown();
    }


    private int getChoice() {
        System.out.println(
                """
                        1. Fetch one SE sale - Unary
                        2. Fetch multiple SE sales - server streaming
                        3. Fetch multiple SE sales batched - client streaming
                        4. Build package - bidirectional streaming""");
        return scanner.nextInt();
    }

    public static void main(String[] args) throws InterruptedException {
        new SeClient().run();
    }
}
