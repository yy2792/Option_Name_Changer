# coding: utf-8

# In[14]:


import re
import datetime

class option_name_changer:
        
        month_dict = {"Jan":1,"Feb":2,"Mar":3,"Apr":4, "May":5, "Jun":6, "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12,"Sept":9}

#Transfer Description to Standard Option format MM/DD/YYYY C(P)STRIKE
#Parameter[optname :Description; front: if there are two number in description,1 take front one, 0 take latter one;
#mmddyy: date format in description,1 mmddyy 0 ddmmyy]
        @classmethod
        def to_option(cls, optname, front = 0, mmddyy = 1):
            date1 = cls.find_date(optname,mmddyy)
            if not date1:
                return "Invalid Date"

            strike = cls.find_fraction(optname)

            if not strike:
                strike = cls.find_strike(optname, front)
                if not strike:
                    return "Invalid Strike"

            type1 = cls.find_type(optname)

            if not type1:
                return "Invalid Type Call & Put"

            return date1 + " " + type1 + strike

        # this function is to get the date part of option description
        @classmethod
        def find_date(cls, optname, flag = 1):
            #flag = 1, mmddyyyy
            #flag = 0, ddmmyyyy
            try:
                reg_ex = re.compile(r'\d+[-\./]\d+[-\./]\d+')
                res = reg_ex.findall(optname)

                if len(res)>0:
                    if len(res) > 1:
                        raise ValueError
                    else: 
                        datestr = res[0]
                        if len(re.split(r'[-\./]', datestr)[0]) == 4:
                            year, month, day = re.split(r'[-\./]', datestr)
                        else:
                            if flag == 1:
                                month, day, year = re.split(r'[-\./]', datestr)
                            elif flag == 0:
                                day, month, year = re.split(r'[-\./]', datestr)

                        if len(day) == 1:
                            day = "0" + day
                        if len(month) == 1:
                            month = "0" + month
                        if len(year) == 2:
                            year = "20" + year

                        return month + "/" + day + "/" + year
				
				#this part takes care of the situation like June 18
                else:
                    for key in cls.month_dict:
                        reg_ex = re.compile(key + r'\s*[-\./]*\d*(?![0-9])',re.IGNORECASE)
                        res = reg_ex.findall(optname)
                        if len(res)==0:
                            continue

                        if len(res) > 1:
                            raise ValueError

                        datestr = res[0]

                        month = str(cls.month_dict[key])

                        if len(month) == 1:
                            month = "0" + month

                        reg_ex = re.compile(r'\d+')  
                        res = reg_ex.findall(datestr)

                        #no year exists
                        if len(res) == 0:
                            raise ValueError("No Year is Given")
                        #more than one year
                        if len(res) > 1:
                            raise ValueError("Too Many Years")

                        year = res[0]

                        if len(year) == 2:
                            year = "20" + year

                        if len(year) > 4:
                            raise ValueError("Invalid Year")

                        datedum = cls.find_thirdFri(int(year), int(month), 1)

                        return datedum.strftime("%m/%d/%Y")
                
				
				
				
				
                #does the string contain 07/09 or 7/9 ...
                if re.search(r'\d+[-\./]\d+', optname, flags=re.IGNORECASE):
                    #if the fraction comes from a strike
                    if re.search(r'\d+\s+\d+\/\d+', optname, flags=re.IGNORECASE):
                        optname2 = re.sub(r'\d+\s+\d+\/\d+', "", optname)
                    else:
                        optname2 = optname
                    
                    reg_ex = re.compile(r'\d+\/\d+', re.IGNORECASE)
                    res = reg_ex.findall(optname2)
                    
                    if len(res) == 1:
                        # assume it is in the form of 06/18
                        datestr = res[0]
                        month, year = re.split(r'[-\./]', datestr)
                        
                        if len(year) == 2:
                            year = "20" + year

                        if len(year) > 4:
                            raise ValueError("Invalid Year")

                        datedum = cls.find_thirdFri(int(year), int(month), 1)

                        return datedum.strftime("%m/%d/%Y")
                    
                    else:
                        raise ValueError
                        
            except ValueError:
                pass
            return False
        
        @classmethod
        def to_int(cls, num2):
            num = float(num2)
            if num == int(num):
                return str(int(num))
            else:
                return str(num)


        #This function returns the type of option (call or put)
        @classmethod
        def find_type(cls, optname):
            try:
                optname = " " + optname + " "
                reg_ex = re.compile(r'(?<=[^a-zA-Z])(Put|Call|C|P)(?![a-zA-Z])',re.IGNORECASE)
                res = reg_ex.findall(optname)

                if len(res) == 0:
                    raise ValueError

                if len(res) > 1:
                    raise ValueError

                optype = res[0]

                if optype.upper() == "PUT":
                    optype = "P"
                elif optype.upper() == "CALL":
                    optype = "C"

                return optype

            except ValueError:
                pass
            return False
        
        @classmethod
        def find_strike(cls, optname, front = 0):
            try:
                #clean all the date
                res = cls.erase_date(optname)

                reg_ex = re.compile(r'(\d+\.*\d*)',re.IGNORECASE)
                res = reg_ex.findall(res)

                if len(res) == 0:
                    raise ValueError("No Strike Price")
                elif len(res) == 1:
                    return cls.to_int(res[0])
                elif len(res) == 2:
                    if front == 1:
                        return cls.to_int(res[0])
                    elif front == 0:
                        return cls.to_int(res[1])
                else:
                    raise ValueError("Confused with strike Price")
            except:
                pass
            return False
        
        @classmethod
        def find_thirdFri(cls, year0, month0, day0):
            wkday = datetime.datetime(year0, month0, day0).weekday() + 1
            daynum = (5-wkday) % 7 + 14
            return datetime.datetime(year0, month0, day0) + datetime.timedelta(days = daynum)

        #Covert frac string to float number,split using / and space
        @classmethod
        def convert_to_float(cls, frac_str):
                try:
                    return float(frac_str)
                except ValueError:
                    num, denom = frac_str.split('/')
                    try:
                        leading, num = re.split('\s+',num)
                        whole = float(leading)
                    except ValueError:
                        whole = 0
                    frac = float(num) / float(denom)
                    return whole - frac if whole < 0 else whole + frac

        #find frac number then convert to decimal,return decimal string
        #parameter: description
        #return False if no fraction or multi fraction 
        @classmethod
        def find_fraction(cls, optname):
            try:
                reg_ex = cls.erase_date(optname)
                frac_num = len(re.findall(r'(\d+\/\d+)',reg_ex))
                if frac_num >1:
                    raise ValueError('Multi Fraction In Description')
                fract = re.findall(r'(\d+\s+\d+\/\d+)',reg_ex)
                if len(fract)>0:
                    if len(fract)>1:
                        raise ValueError
                    else:
                        return str(round(cls.convert_to_float(fract[0]),4))
                else:
                    fract = re.findall(r'(\d+\/\d+)',reg_ex)
                    if len(fract)>0:
                        if len(fract)>1:
                            raise ValueError
                        else:
                            return str(round(cls.convert_to_float(fract[0]),4))
                    else:
                        return False
            except ValueError:
                return False

        @classmethod
        def erase_date(cls, optname):
            try:     
                
                res = re.sub(r'\d+[-\./]\d+[-\./]\d+', "", optname)
                # if optname contains date, no need to check further, we assume there is only one date
                if len(res) < len(optname):
                    return res

                for key in cls.month_dict:
                        if re.search(key + r'\s*[-\./]*\d*(?![0-9])', res, flags=re.IGNORECASE):
                            res = re.sub(key + r'\s*[-\./]\d*(?![0-9])', "", res, flags=re.IGNORECASE)
                # if optname contains date, no need to check further, we assume there is only one date
                if len(res) < len(optname):
                    return res
                
                if re.search(r'\d+[-\./]\d+', optname, flags=re.IGNORECASE):
                    #if the fraction comes from a strike
                    if re.search(r'\d+\s+\d+\/\d+', optname, flags=re.IGNORECASE):
                        # if it has a fraction strike and a date form mm/yy(yy), we need only to replace mm/yy part
                        
                        reg_ex = re.compile(r'\d+\/\d+', re.IGNORECASE)
                        temp = reg_ex.findall(optname)
                        
                        if len(temp)>2:
                            raise ValueError
                        # the only fraction follows with strike
                        elif len(temp) == 1:
                            res = optname
                        # both fraction and date
                        else:
                            start1 = re.search(r'\d+\/\d+', optname, flags=re.IGNORECASE).start()
                            start2 = re.search(r'\d+\s+\d+\/\d+', optname, flags=re.IGNORECASE).start()
                            
                            #we need to find where the fraction lays in the strike
                            reg_ex = re.compile(r'\d+\s+\d+\/\d+', re.IGNORECASE)
                            temp_strike = reg_ex.findall(optname)
                            
                            if len(temp_strike) > 2:
                                raise ValueError
                            
                            start3 = re.search(r'\d+\/\d+', temp_strike[0], flags=re.IGNORECASE).start()
                                
                            indxm = [m.span() for m in re.finditer(r'\d+\/\d+', optname, flags=re.IGNORECASE)]
                            
                            if start1 == start2 + start3:
                                rept = temp[1]
                                start, end = indxm[1]
                                                               
                            elif start1 < start2 + start3:
                                rept = temp[0]
                                start, end = indxm[0]
                  
                            res = optname[:start] + optname[end:]
                        
                    else:
                        res = re.sub(r'\d+\/\d+',"",optname)
                    
                return res
            
            except ValueError:
                pass
            return False
