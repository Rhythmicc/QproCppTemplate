#include <iostream>
#include <msg.h>
using namespace std;

int main(int argc, char **argv)
{
    echo(info, "Hello World!");
    echo(success, "Success!");
    echo(debug, "Debug!");
    echo(error, "Error!");
    echo(split, "Split!");
    return 0;
}
