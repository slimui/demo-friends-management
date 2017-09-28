#! /bin/sh

echo 'Compiling relay schema'

BASEDIR=$(dirname $0)

relay-compiler --schema $BASEDIR/schema/schema.json --src $BASEDIR/src
