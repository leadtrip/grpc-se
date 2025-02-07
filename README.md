### Description
A GRPC based project that exercises both Java and Python

### setup
Generate the Java and Python GRPC code from the proto file

`mvn clean install`

There are 3 saved run configurations, first start the Python server 'se_server'.

Then try each of the Python and Java clients 'se_client' and SeClient.

Both clients offer ways to test both unary and server streaming options.