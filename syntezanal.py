#from tkinter import*
import math, array
#window = Tk()
#window.title("GNU Синтез и анализ рабочего цикла")

#Вводим данные
Press0 = 0.1013    #Press0 = float(input("Давление окружающей среды, МПа")) #Давление окружающей среды, МПа 
Temp0 = 293.0      #Temp0 = float(input("Температура окружающей среды, К")) #Температура окружающей среды, К
Comprat = 14.0     #Степень сжатия
CrankRod = 0.2703  #Отношение радиуса кривошипа к длине шатуна
Pressgas = 0.1445  #Давление остаточных газов, МПа
Tempgas = 850.0    #Температура остаточных газов, К
Fill = 0.92        #Коэффициент наполнения
Charheat = 10.0    #Подогрев заряда, К
CompPoly = 1.38    #Политропа сжатия
ExtenPoly = 1.35   #Политропа расширения
Compress = 0.20    #Давление наддува, МПа
PolyComp = 1.6     #Политропа сжатия в компрессоре
TempReduc = 25.0   #Понижение температуры в ОНВ, К
CrankRevo = 1250.0 #Обороты коленвала, об/мин
Cylvolume = 3.620  #Объём цилиндра, м3
#Вводим дополнительные данные
LowHeat = 42.50      #Низшая теплота сгорания топлива, МДж/кг
Carbonmass = 0.86    #Массовая доля углерода в топливе
Hydromass = 0.13     #Массовая доля водорода в топливе
Oxygenmass = 0.01    #Массовая доля кислорода в топливе
Excessfuel = 1.65    #Коэффициент избытка воздуха
IgniAdvAng = -10.0   #Угол опережения воспламенения, ГРАД ПКВ
Combefficrat = 0.87  #Коэффициент эффективности сгорания
HeatDiss = 0.0       #Коэффициент тепловыделения
InitCombDurat = 10.0 #Продолжительность начального периода сгорания, ГРАД ПКВ
InitCombus = 0.02    #Показатель характера сгорания в начальном периоде
MainCombDurat = 110.0#Продолжительность основного периода сгорания, ГРАД ПКВ
MainCombus = 0.30    #Показатель характера сгорания в основном периоде
IntaValvLag = -10.0  #Угол запаздывания закрытия впускного клапана, ГРАД ПКВ
ExhValvOpen = 15.0   #Угол открытия выпускного клапана,ГРАД ПКВ
Fph = 9.14           #Часовой расход топлива, кг/час

#Процесс Синтеза и Анализа
#Процесс Впуска
TempAfterComp = Temp0 * (Compress/Press0)**((PolyComp + 1) / PolyComp) #Температура воздуха после компрессора
TempAfterReduc = TempAfterComp - TempReduc #Температура воздуха после охладителя наддува
Resgas = (Pressgas * TempAfterReduc)/(Compress * Tempgas * (Comprat - 1) * Fill) #Коэффициент остаточных газов (РЕЗУЛЬТАТ!)

#Теоретические массы топлива
TheorAir1 = ((8 * Carbonmass) / 3 + 8 * Hydromass - Oxygenmass) / 0.232 #Теоретически необходимое количество воздуха'
TheorAir = (Carbonmass / 12 + Hydromass / 4 - Oxygenmass / 32) / 0.21 #Теоретически необходимое количество воздуха

#Параметры рабочего тела в начале сжатия
PressA = (Fill * Compress * (Comprat - 1) * (TempAfterReduc - Charheat) / TempAfterReduc + Pressgas)/Comprat #Давление в начале такта сжатия
TempA = (TempAfterReduc + Charheat + Resgas * Tempgas) / (1 + Resgas) #Температура рабочего тела в начале такта сжатия
MolecMassA = TheorAir1 / TheorAir #Молекулярная масса в конце впуска
VolA = 0.008314 * TempA / (PressA * MolecMassA) #Объём рабочего тела в начале такта сжатия

#Параметры рабочего тела в конце сжатия/начале сгорания
VolY = VolA / Comprat #Объём рабочего тела в конце сжатия
PressY = PressA * ((VolA / VolY) ** CompPoly)#Давление рабочего тела в конце сжатия
TempY = TempA *((VolA / VolY) ** (CompPoly - 1)) #Температура рабочего тела в конце сжатия
MolecMassY = 0.008314 * TempY / (PressY * VolY) #Молекулярная масса в конце сжатия/начале сгорания (РЕЗУЛЬТАТ!)

#Расчёт необходимых переменных
MaxChem = 1 + ((Hydromass / 4) + (Oxygenmass / 32)) / (Excessfuel * TheorAir) #Максимальное значение химического коэффициента молекулярного изменения (РЕЗУЛЬТАТ!)
MaxValid = (MaxChem + Resgas) / (1 + Resgas) #Максимальное значение действительного коэффициента молекулярного изменения (РЕЗУЛЬТАТ!)
AmountHeatZ = (Combefficrat * LowHeat) / ((1 + Resgas) * Excessfuel * TheorAir1 + 1) #Общая удельная использованная теплота сгорания (РКЗУЛЬТАТ!)
MolecMassZ = MolecMassY / MaxValid #Молекулярная масса рабочего тела в конце сгорания (РЕЗУЛЬТАТ!)

BeginFire = 360 + IgniAdvAng #Начало сгорания в ГРАД
EndFire = 360 + IgniAdvAng + MainCombDurat # Конец сгорания в ГРАД

#Задаём диапазон для массива производной функции для массива объёмов
j = list(range(0, 144))
Psi = list(range(0, 144))
Vol = list(range(0, 144))
Press = list(range(0, 144))
Temp = list(range(144))
PresSpeed = list(range(144))
CompPolyAnal = list(range(144))
ExtenPolyAnal = list(range(144))
WorkComp = list(range(144))
WorkExten = list(range(144))
Chem = list(range(144))
MidChem = list(range(144))
MolMass = list(range(144))
x = list(range(144))
xSpeed = list(range(144))
Work = list(range(144))
k = list(range(144))
PressA1 = VolA1 = PressZ = VolZ = TempZ = PressB = VolB = i = WorkAY = WorkYZ = WorkZB = 0
for j in list(range(144)):
    i = 180 + (j * 2.5) #Угол в ГРАД
    ic = (math.pi * i) / 180 #Угол в РАД  3.1415
    Psi[j] = 1 + ((Comprat - 1) / 2) * (1 + (1 / CrankRod)) - (math.cos(ic) + (1 / CrankRod) * \
    math.sqrt(1 - (CrankRod ** 2) * math.sin(ic))) #Производная для расчёта объёмов

#Процесс сжатия
    if i < BeginFire:
        #Массивы Объёмов, Давлений и Температур
        Vol[j] = VolA * CrankRod * Psi[j]
        Press[j] = PressA * ((VolA / Vol[j]) ** (CompPoly))
        Temp[j] = TempA * ((VolA / Vol[j]) ** (CompPoly - 1))
    #Задаём условие расчёта нарастания давления
    if j == 0:
        PresSpeed[j] = (Press[j] - PressA) / (i - (i - 2.5))
    elif j!= 0:
        PresSpeed[j] = (Press[j] - Press[j-1]) / (i - (i - 2.5))
    #Считаем работу такта сжатия
    WorkAY = (PressA * VolA - PressY * VolY) / (CompPoly -1) #(РЕЗУЛЬТАТ!)

    #Анализируем политропу и работу такта сжатия
    if i == BeginFire + IntaValvLag:
        PressA1 = Press[j]
        VolA1 = Vol[j]
    if i < BeginFire:
        CompPolyAnal[j] = math.log10 (Press[j] / Press[j-1]) / math.log10 (Vol[j-1] / Vol[j]) #Политропа сжатия на элементарных участках
        WorkComp[j] = (Press[j-1] * Vol[j-1] - Press[j] * Vol[j]) / (CompPolyAnal[j] - 1) #Удельная работа на элементарных участках от закрытия впускного клапана до воспламенения
        z = list(WorkComp)
        WorkA1Y = sum (z)
        CompPolyAnall = (PressA1 * VolA1 - PressY * VolY) / (WorkA1Y) + 1 #Анализ политропы сжатия (РЕЗУЛЬТАТ!АНАЛИЗ)
        WorkAA1 = (PressA * VolA - PressA1 * VolA1) / (CompPolyAnall - 1)
        WorkAYanal = WorkAA1 + WorkA1Y #Удельная работа процесса сжатия (РЕЗУЛЬТАТ!АНАЛИЗ)

        #Процесс сгорания сдвинуть все ниже
        fi = i - BeginFire #Угол от начала воспламенения
            if i == BeginFire:
                x = xSpeed = 0.0000
            if i == EndFire:
                x = 0.9999
        #Условие расчёта выгорания топлива
        if fi > 0 and fi <= MainCombDurat:
            if fi > InitCombDurat:
                InitCombus = MainCombus
                x = 1 - math.exp (-6.908 * (fi / InitCombDurat) ** (InitCombus - MainCombus) * (fi / MainCombDurat) ** (MainCombus + 1)) #Доля выгоревшего топлива
                xSpeed = 6.908 * ((InitCombus + 1) / MainCombDurat) * (fi / InitCombDurat) ** (InitCombus - MainCombus) * \
                (fi / MainCombDurat) ** (MainCombus) * math.exp (-6.908 * (fi / InitCombDurat) **(InitCombus - MainCombus) * (fi / MainCombDurat) ** (MainCombus + 1)) #Скорость выгорания топлива
            elif InitCombDurat <= i <= MainCombDurat:
                 InitCombus != MainCombus
                 x = 1 - math.exp (-6.908 * (fi / InitCombDurat) ** (InitCombus - MainCombus) * (fi / MainCombDurat) ** (MainCombus + 1))
                 xSpeed = 6.908 * ((InitCombus + 1) / MainCombDurat) * (fi / InitCombDurat) ** (InitCombus - MainCombus) * \
                (fi / MainCombDurat) ** (MainCombus) * math.exp(-6.908 * (fi / InitCombDurat) **(InitCombus - MainCombus) * (fi / MainCombDurat) ** (MainCombus + 1))
        if i >= BeginFire and i <= EndFire:
            if i == BeginFire:
                k[j-1] = 1.259 + (76.7 / TempY) #Отношение теплоёмкостей в начале сгорания
                x[j-1] = 1 - math.exp (-6.908 * (2.5 / InitCombDurat) ** (InitCombus - MainCombus) * (2.5 / MainCombDurat) ** (MainCombus + 1))
                Chem[j] = 1 + (MaxValid - 1) * x #Изменение молекулярной массы на участке
                Chem[j-1] = 1 + (MaxValid - 1) * x[j-1]
                MidChem[j] = (Chem[j] + Chem[j-1]) / 2 #Среднее значение изменения молекулярной массы на участке
                MolMass[j] = MolecMassY / Chem[j] #Молекулярная масса на участке
                MolMass[j-1] = MolecMassY / Chem[j-1]
                if Excessfuel > 1 and LowHeat == 43.8:
                    k = 1.259 + (76.7 + 0.6 * x) * 1 / Temp - x * (0.012 - 0.03 / Excessfuel) #Отношение теплоёмкостей для продуктов сгорания бензиновых фракций (Excessfuel > 1)
                if Excessfuel > 1 and LowHeat == 42.5:
                    k = 1.259 + 76.7 / Temp - x * (0.05 + 0.0372 / Excessfuel) #Отношение теплоёмкостей для продуктов сгорания дизельных фракций
                #Массивы Объёмов, Давлений и Температур
                Vol[j] = VolA * CrankRod * Psi[j]
                Press[j] = Chem[j] * (((PressY * AmountHeatZ * k - 1) * MolMass * x[j]) / (TempY * 0.008314) + PressY) * (VolY / Vol[j]) ** k[j]
                Temp[j] = (Press[j] * Vol[j] * MolecMassY) / (0.008314 * Chem[j])
            elif BeginFire < i <= EndFire:
                 dx = x[j] - x[j-1] #Разница долей выгоревшего топлива
                 Chem[j] = 1 + (MaxValid - 1) * x #Изменение молекулярной массы на участке
                 MolMass[j] = MolecMassY / Chem[j] #Молекулярная масса на участке
                 if Excessfuel > 1 and LowHeat == 44.0:
                     k[j] = 1.259 + (76.7 + 0.6 * x) / Temp[j] - x[j] * (0.012 - 0.03 / Excessfuel) #Отношение теплоёмкостей для продуктов сгорания бензиновых фракций (Excessfuel > 1)
                 if Excessfuel > 1 and LowHeat == 42.5:
                     k[j] = 1.259 + 76.7 / Temp - x[j] * (0.05 + 0.0372 / Excessfuel) #Отношение теплоёмкостей для продуктов сгорания дизельных фракций
        #Массивы Объёмов, Давлений и Температур
        Vol[j] = VolA * CrankRod * Psi[j]
        Press[j] = Chem[j] * (((PressY * AmountHeatZ * k[j-1]) * MolMass[j] * x[j]) / (TempY * 0.008314) + PressY) * (VolY / Vol[j]) ** k[j]
        Temp[j] = (Press[j] * Vol * MolecMassY) / (0.008314 * Chem[j])
        X = sum (math.log (-2.303 * math.log(1 - x[j])) - math.log (6.908))
        Y = sum (math.log (fi))
        Midk = (k[j] + k[j-1]) / 2 #Среднее значение отношений теплоёмкостей на участках
        PresSpeed = (Press[j] - Press[j-1]) / (i - (i - 2.5)) #Скорость нарастания давления

        #Считаем работу такта сгорания методом трапеций
        Work[j] = 0.5 * (Press[j-1] + Press[j]) * (Vol[j] - Vol[j-1]) #Работа на элементарных участках
        zz = list(Work)
        WorkYZ = sum (zz) #Удельная работа такта сгорания (РЕЗУЛЬТАТ!СИНТЕЗ!АНАЛИЗ)

        #Анализ процесса сгорания
        Time = EndFire - BeginFire + 1 #Количество тактов в сгорании
        A = (Y - (1 / (MainCombus + 1)) * X) / Time
        MainCombDuratAnal = 10 ** A #Продолжительность сгорания (РЕЗУЛЬТАТ!АНАЛИЗ)
        CombefficratNEW = 1 - 2.38 * (MainCombDuratAnal / Time * Excessfuel) #НОВИЗНА Коэффициент эфективности сгорания (РЕЗУЛЬТАТ!АНАЛИЗ)
        AmountHeatZNEW = (CombefficratNEW * LowHeat) / ((1 + Resgas) * Excessfuel * TheorAir1 + 1) #Удельная использованная теплота сгорания (РЕЗУЛЬТАТ!АНАЛИЗ)
#Параметры рабочего тела в конце такта сгорания
if i == EndFire:
        VolZ = Vol[j], PressZ = Press[j], TempZ = Temp[j]     

#Процесс Расширения
if i > EndFire:
        Vol[j] = VolA * CrankRod * Psi[j]
        Press[j] = PressZ * (VolZ / Vol[j]) ** ExtenPoly
        Temp[j] = TempZ * (VolZ / Vol[j]) ** (ExtenPoly - 1)
        PresSpeed = (Press[j] - Press[j- 1]) / (i - (i - 2.5))
        PressB = PressZ * (VolZ / VolA) ** ExtenPoly #Давление в конце расширения
#Считаем работу такта расширения
WorkZB = (PressZ * VolZ - PressB * VolA) / (ExtenPoly - 1) #(РЕЗУЛЬТАТ)

#Анализируем политропу и работу такта расширениястриминг звуком с компьютера при звонках
if i == 540 - ExhValvOpen:
    PressB = Press[j], VolB = Vol[j]
    if i - EndFire < 1.25:
        ExtenPolyAnal[j] = math.log10 (Press[j-1] / Press[j]) / math.log10 (Vol[j] / Vol[j-1]) #Политропа расширения от окончания сгорания до НМТ поршня 
        WorkExten[j] = (Press[j-1] * Vol[j-1] - Press[j] * Vol[j]) / ExtenPolyAnal[j-1] #Работа на элементарных участках
    else:
        ExtenPolyAnal[j] = math.log10 (Press[j-1] / Press[j]) / math.log10 (Vol[j] / Vol[j-1]) #Политропа расширения от окончания сгорания до НМТ поршня 
        WorkExten[j] = (Press[j-1] * Vol[j-1] - Press[j] * Vol[j]) / ExtenPolyAnal[j-1] #Работа на элементарных участках
zzz = list(WorkExten)
WorkZBanal = sum (zzz) #Работа такта расширения (РЕЗУЛЬТАТ!АНАЛИЗ)
ExtenPolyAnal1 = (PressZ * VolZ - PressB * VolB) / WorkZBanal + 1 #Политропа расширения (РЕЗУЛЬТАТ!АНАЛИЗ)     

#Оценка качества сгорания по частным критериям:
kfi = (MainCombDurat - 50) / 50                                                        #Продолжительности
kkes = (1 - Combefficrat) / 1                                                          #Адиабатности
kteta = (19 + IgniAdvAng) / 19                                                         #Своевременности
km = (2 - MainCombus) / 2 							                                   #Характерности
kdm = math.atan((MainCombus - InitCombus) / ((MainCombus + 1) * (InitCombus + 1) + 1)) #Монотонности
#Оценка качества сгорания по комплексным критериям:
ke = 0.87 * kkes + 0.07 * kfi + 0.04 * kteta + 0.01 * km + 0.01 * kdm                  #Экономичности
kMm = 0.87 * kkes + 0.07 * kfi + 0.04 * kteta + 0.01 * km + 0.01 * kdm                 #Мощности
kp = 0.86 * kkes + 0.12 * kfi + 0.14 * kteta + 0.03 * km + 0.03 * kdm                  #Механической нагруженности
kt = 0.72 * kkes + 0.12 * kfi + 0.12 * kteta + 0.02 * km + 0.02 * kdm                  #Тепловой нагруженности

#Определение индикаторных показателей рабочего цикла по индикаторной диаграмме
IndiWork = WorkAY + WorkYZ + WorkZB #Мощность
IndiPress = (Comprat * IndiWork) / ((Comprat - 1) * VolA) #Давление
IndiEfficiency = (Combefficrat * IndiWork) / AmountHeatZ #КПД
IndiFuel = 3600/(LowHeat * IndiEfficiency) #Удельный расход топлива 
print(IndiWork, IndiPress, IndiEfficiency, IndiFuel)
#window.mainloop()
