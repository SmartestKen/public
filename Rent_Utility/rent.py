import os
try:
    os.remove('/home/public/Rent_Utility/rent.txt')
except Exception:
    pass
with open('/home/public/Rent_Utility/rent.txt', 'a') as file:
    file.write("rent for current month, utility for previous month\n")
    file.write('        Kyra             Udai          Keren        Sejal\n')

    rent = 2568.76
    file.write('Jul     %7.3f       %7.3f       %7.3f       %7.3f\n'%(
                rent*0.3, rent*0.5, rent*0.2, 0))


    rent = 2503.53
    utility = 204.48
    file.write('Aug     %7.3f       %7.3f       %7.3f       %7.3f\n'%(
                rent*0.3+utility*0.334, rent*0.5+utility*0.334, rent*0.2+utility*0.334, 0))


    rent = 2565.27
    utility = 82.13
    file.write('Sep     %7.3f       %7.3f       %7.3f       %7.3f\n'%(
                rent*0.3+utility*0.334, rent*0.5+utility*0.334, rent*0.2+utility*0.334, 0))


    rent = 2523.04
    utility = 81.47
    extra = 2565.27*0.5+82.13*0.334-1200
    file.write('Oct     %7.3f        %7.3f       %7.3f         %7.3f\n'%(
                rent*0.3+utility*0.3, rent*0.25+utility*0.3+extra, rent*0.2+utility*0.3, rent*0.25+utility*0.1))
    # print(rent*0.3+utility*0.3+rent*0.25+utility*0.3+rent*0.2+utility*0.3+rent*0.25+utility*0.1-rent-utility)

    cleaner = 65.38
    file.write('Cleaner %7.3f       %7.3f       %7.3f         %7.3f\n'%(
                cleaner*0.25, cleaner*0.25, cleaner*0.25, cleaner*0.25))
    rent = 2527.59
    utility = 77.10
    file.write('Nov     %7.3f        %7.3f       %7.3f         %7.3f\n'%(
                rent*0.3+utility*0.25, rent*0.25+utility*0.25, rent*0.2+utility*0.25, rent*0.25+utility*0.25))

    rent = 2589.42
    utility = 113.14
    file.write('Dec     %7.3f        %7.3f       %7.3f         %7.3f\n'%(
                rent*0.3+utility*0.25, rent*0.25+utility*0.25, rent*0.2+utility*0.25, rent*0.25+utility*0.25))



    rent = 2509.05+5
    utility = 95.96

    file.write('Jan_pre %7.3f     %7.3f       %7.3f         %7.3f\n'%(
                750, 600, 0, 600))
    file.write('Jan_post %7.3f    %7.3f       %7.3f         %7.3f\n'%(
                rent*0.3+utility*0.25-750, rent*0.25+utility*0.25-600, rent*0.2+utility*0.25, rent*0.25+utility*0.25-600))



    rent = 2494.57
    utility = 120.65
    file.write('Feb    %7.3f        %7.3f       %7.3f         %7.3f\n'%(
                rent*0.3 + utility*0.25, rent*0.25 + utility*0.25, rent*0.2 + utility*0.25, rent*0.25 + utility*0.25))


    # +31.75 due to reverse late fee (i.e. get back my payment and re-distribute)
    # +10 for (+5+5) Feb and Mar insurance fee
    rent = 2437.45 + 31.75 + 10
    utility = 97.72
    file.write('Mar    %7.3f        %7.3f       %7.3f         %7.3f\n'%(
                rent*0.3 + utility*0.25, rent*0.25 + utility*0.25, rent*0.2 + utility*0.25, rent*0.25 + utility*0.25))


    rent = 2505.92 + 5
    utility = 89.83
    file.write('April    %7.3f        %7.3f       %7.3f         %7.3f\n' % (
                rent * 0.3 + utility * 0.25, rent * 0.25 + utility * 0.25, rent * 0.2 + utility * 0.25, rent * 0.25 + utility * 0.25))


    rent = 2501.73 + 5
    utility = 56.47
    file.write('May    %7.3f        %7.3f       %7.3f         %7.3f\n' % (
                rent * 0.3 + utility * 0.5, rent * 0.25 + utility * 0, rent * 0.2 + utility * 0.5, rent * 0.25 + utility * 0))


    rent = 2504.21*22/30 + 5
    utility = 60.45*22/30
    file.write('June_p1   %7.3f        %7.3f       %7.3f         %7.3f\n' % (
                rent * 0.3 + utility * 0.5, rent * 0.25 + utility * 0, rent * 0.2 + utility * 0.5, rent * 0.25 + utility * 0))

    rent = 2504.21*8/30
    utility = 60.45*8/30
    file.write('June_p2    %7.3f      %7.3f       %7.3f         %7.3f\n' % (
                rent * 0.35 + utility * 0.5, rent * 0 + utility * 0, rent * 0.25 + utility * 0.5, rent * 0.4 + utility * 0))

    file.write("--------------------------------------------------------------\n")
    file.write("rent for current month, utility for previous month -> \nsimply treat everything current month to avoid errors\n")

    rent = 2504.21*8/30
    utility = 60.45*8/30
    file.write('        Kyra           Spencer          Keren        Sejal\n')
    file.write('June_p2 %7.3f      %7.3f       %7.3f         %7.3f\n' % (
                0, rent*0.25 + utility*0.5, 0, 0))

    rent = 2500.31
    utility = 73.05
    file.write('July    %7.3f      %7.3f       %7.3f         %7.3f\n' % (
                rent*0.3+utility*0.25, rent*0.25+ utility*0.5, rent*0.2+utility*0.25, rent*0.25+utility*0))
    
    # -5 for key +10 for insurance
    rent = 2564.68 - 5 + 10
    utility = 138.59
    key = 5
    file.write('Aug    %7.3f      %7.3f       %7.3f         %7.3f\n' % (
                rent*0.3+utility*0.25, rent*0.25+ utility*0.5+key, rent*0.2+utility*0.25, rent*0.25+utility*0))    
    
    rent = 2564.72 + 10
    utility = 76.36

    file.write('Sep_p1    %7.3f      %7.3f       %7.3f         %7.3f\n' % (
                rent*(5/30)*0.3+utility*(5/30)*0.33, rent*(5/30)*0.25+ utility*(5/30)*0.33, rent*(5/30)*0.2+utility*(5/30)*0.33, rent*(5/30)*0.25+utility*(5/30)*0))
    file.write("\n")
    file.write('        Kyra         Brendan         Keren        Sejal\n')
    file.write('Sep_p2    %7.3f      %7.3f       %7.3f         %7.3f\n' % (
                rent*(25/30)*0.35+utility*(25/30)*0.5, 0, rent*(25/30)*0.25+utility*(25/30)*0.5, rent*(25/30)*0.4+utility*(25/30)*0))


    rent = 2510.12 + 5
    utility = 65.08
    file.write('Oct    %7.3f      %7.3f       %7.3f         %7.3f\n' % (
        rent * 0.3 + utility * 0.33, rent * 0.25 + utility * 0.33, rent * 0.2 + utility * 0.33,
        rent * 0.25 + utility * 0))

    rent = 2560.95 + 5
    utility = 73.44
    file.write('Nov    %7.3f      %7.3f       %7.3f         %7.3f\n' % (
        rent * 0.3 + utility * 0.3, rent * 0.25 + utility * 0.2, rent * 0.2 + utility * 0.3,
        rent * 0.25 + utility * 0.2))

    rent = 2510.81 + 5
    utility = 73.97
    file.write('Dec    %7.3f      %7.3f       %7.3f         %7.3f\n' % (
        rent * 0.3 + utility * 0.4, rent * 0.25 + utility * 0.2, rent * 0.2 + utility * 0.4,
        rent * 0.25 + utility * 0))

    rent = 2516.91 + 5
    utility = 73.97
    file.write('Jan    %7.3f      %7.3f       %7.3f         %7.3f\n' % (
        rent * 0.3 + utility * 0.4, rent * 0.25 + utility * 0.2, rent * 0.2 + utility * 0.4,
        rent * 0.25 + utility * 0))