# ItchyLang
~~*(probably I should consider other names, but keep in mind there were worse ideas)*~~


---
### About
*Author: Vitalii Khomyn, PMI-45*\
*Graduation project for Lviv National University*
*Theme: "Components of the programming system. The development of a translator from the input programming language"*
---
### The main idea of entire project:
Write a translator (compiler in this case) ~~as far as possible~~ for custom programming language I made up.\
Why? Because it's fun :-) Possibility to deep into the hood of most programming languages (at least high-level ones).
---
## The concept of language
The "ItchyLang" is general-purpose imperative multi-paradigm 
(for now, it's procedural and object-oriented) programming language, with syntax inspired mainly from Python, C++,
JavaScript and some other existing languages.\

Example of code (concept considering what's done now) looks like this:
```itchylang


function bubble_sort(reference array[float, ?] arr)
{
    integer array_length := arr->length();
    
    integer i := 0;
    while (i < array_length)
    {
        integer j := 0;
        float buffer;
        boolean swapped := false;
        
        while (j < array_length - 1 - i) {
            if (arr[j] > arr[j+1]) {
                buffer := arr[j];
                arr[j] := arr[j+1];
                arr[j+1] := buffer;
                swapped := true;
            }
            j := j + 1;
        }
        if (swapped) {
            break;
        }
        i := i + 1;
    }
} 

function[float] sum_of_elements(const reference array[float, ?] arr)
{
    integer length := arr->length();
    float _sum := 0;
    
    integer i := 0;
    while (i < length) {
        _sum := _sum + arr[i];
        i := i + 1; 
    }
    return _sum;
}

function Main()
{
    array[float, 7] x := [-3, -1.3, 4, 5, 3.2, 0, 4];
    print(sum_of_elements(reference x));
    bubble_sort(reference x);
    print(x);
}

Main();

```
(the docs will be continued later)