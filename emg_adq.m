clc; clean all; clear all; 

%% Cargar los datos del archico de texto  
data = importdata('REGISTRO');

%% Obtención de Columnas de Datos 
num_data = data(:,1);   
emg1_data = data(:,2);
emg2_data = data(:,3);

%% Tiempo de Inicio y Tiempo Final
t_I = 10;   %Tiempo Inicial
t_F = 100;  %Tiempo Final

%% Indice correspondiente de Tiempo inicial y final
fs = 1;     %Frecuencia de muestreo 
ind_I = t_I * fs;    %Indice de tiempo inicial
ind_F = t_F * fs - 1;    %Indice de tiempo final

%% Ventana de recorte Emg 1
Emg1_rec = emg1_data (ind_I:ind_F);     %Ventana de recorte 
t1 = t_I:1/fs:t_F-1/fs;     %Tiempo de Ventana recortada 

%% Ventana de Recorte Emg 2
Emg2_rec = emg2_data (ind_I:ind_F);     %Ventana de recorte
t2 = t_I:1/fs:t_F-1/fs;     %Tiempo de Ventana recortada 

%% Señal Emg 1 Recortada
figure(1);
subplot(2,2,3);
plot(t1,Emg1_rec,'LineWidth',1);
title('Electromiograma 1 Recortado');
xlabel('Tiempo');
ylabel('Amplitud');
axis tight;

%% Señal Emg 2 Recortada
figure(2);
subplot(2,2,4);
plot(t2,Emg2_rec,'LineWidth',1);
title('Electromiograma 2 Recortado');
xlabel('Tiempo');
ylabel('Amplitud');
axis tight;

%% Graficación de valor Emg 1 en Función del número de dato 
subplot(2,2,1);
plot(num_data,emg1_data);
xlabel('Número de dato');
ylabel('Registro Electromiograma 1');
title('Gráfico del valor Electromiograma 1');

%% Graficación de valor Emg 2 en Función del número de dato 
subplot(2,2,2);
plot(num_data,emg2_data);
xlabel('Número de dato');
ylabel('Registro Electromiograma 2');
title('Gráfico del valor Electromiograma 2');

%% Ajuste de Disposición de las Graficas
sgtitle('Gráficas de EMG', 'FontSize',18);

%% Guardar las Gráficas em archivos de imagen 
saveas(gcf,'graficas_emg.png');



































