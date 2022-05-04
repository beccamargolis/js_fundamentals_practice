//1. Multiples of Three – but Not All
//Using FOR, print multiples of 3 from -300 to 0. Skip -3 and -6.

for (var num = -300; num <= 0; num += 3)
    {
        if (num == -3 || num == -6)
        {
            continue;
        }
console.log(num);
}

//2. Printing Integers with While
//Print integers from 2000 to 5280, using a WHILE.

var num = 2000;
while (num <= 5280)
{
    console.log(num);
    num = num + 1;
}

//3. Counting, the Dojo Way
//Print integers 1 to 100. If divisible by 5, print "Coding" instead. If by 10, also print " Dojo".

for (var num = 1; num <= 100; num += 1)
    {
        if (num % 10 == 0)
        {
            console.log("Coding Dojo")
        }
        else if (num % 5 == 0)
        {
            console.log("Coding")
        }
        else
        {
            console.log(num)
        }
    }

//4. Flexible Countdown
//Given lowNum, highNum, mult, print multiples of mult from highNum down to lowNum, using a FOR.
//For (2,9,3), print 9 6 3 (on successive lines).

function findMultiples(lowNum, highNum, mult) {               
    for (var num = highNum; num >= lowNum; num = num - mult)
    {                   
        console.log(num);
    }
}
findMultiples(2,9,3);