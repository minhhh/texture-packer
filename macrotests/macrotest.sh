#!/bin/bash

# Copyright 2014 Ha Huy Minh
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

TESTDIR=~+/`dirname $0`
cd $TESTDIR
echo $TESTDIR

export IMAGEPACKER="$TESTDIR/../out/ImagePacker.jar"

testcases=`ls test_*.sh`
echo $testcases

if [ "$1" != "" ]; then
    testcases="$@"
fi

for testcase in $testcases; do
    echo -n "Executing $testcase..."
    TMPDIR=`mktemp -d "imagepacker-${testcase}.XXXXXX"`
    OUTPUT="${TMPDIR}.log"
    # ( cd $TMPDIR && . $TESTDIR/${testcase} >$OUTPUT 2>&1 ) ||
    ( cd $TMPDIR && source $TESTDIR/${testcase} ) ||
        {
	    cat $TMPDIR/$OUTPUT
	    echo "*** Test case $testcase failed ($TMPDIR)"
	    echo "*** Output in $OUTPUT"
	    exit 1
        }
    rm -r $TMPDIR || { echo "Couldn't clean up after test"; exit 1; }
    echo " OK"
done

echo "ALL TESTS COMPLETED"
