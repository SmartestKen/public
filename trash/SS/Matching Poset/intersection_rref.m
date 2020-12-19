clear all; clc
format compact
A = [1,1,2,3
    2,2,1,5];
B = [1,3,4,6
    2,5,1,3
    4,6,7,8];


ha = null([null(A)';null(B)'])';

rank(A) == rank([A; ha]);
rank(B) == rank([B;ha]);