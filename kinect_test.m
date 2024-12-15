clc; clear all; close all;

% Reiniciar adquisición de imágenes
imaqreset;

% Crear un objeto de video color y profundidad
colorVid = videoinput('kinect',1,'RGB_640x480');
depthVid = videoinput('kinect',2,'Depth_320x240');

% Configurar el objeto de video
set(colorVid, 'FramesPerTrigger',1);
set(depthVid, 'FramesPerTrigger',1);
set([colorVid depthVid], 'TriggerRepeat',Inf);
triggerconfig([colorVid depthVid], 'manual');

% Iniciar los objetos de video
start([colorVid depthVid]);

% Crear una figura para la visualización
hFig = figure;

% Capturar y procesar datos del esqueleto
while ishandle(hFig)
    % Capturar una imagen de profundidad
    trigger([colorVid depthVid]);
    colorImage = getdata(colorVid);
    depthImage = getdata(depthVid);

    % Obtener el primer esqueleto detectado
    skeleton = metaData.IsSkeletonTracked;

    if any(skeleton)
        % Posiciones de los hombros
        shoulderLeft = metaData.JointWorldCoordinates(5,:,skeleton);
        shoulderRight = metaData.JointWorldCoordinates(9,:,skeleton);

        % Mostrar la imagen de profundidad
        imshow(depthImage, [0 4096]);
        hold on;

        % Dibujar los puntos de los hombros
        plot(shoulderLeft(1), shoulderLeft(2), 'r*', 'MarkerSize', 10);
        plot(shoulderRight(1), shoulderRight(2), 'r*', 'MarkerSize', 10);

        % Mostrar las posiciones de los hombros en la consola
        disp(['Shoulder Left: X=', num2str(shoulderLeft(1)), ', Y=', num2str(shoulderLeft(2)), ...
            ', Z=', num2str(shoulderLeft(3))]);
        disp(['Shoulder Right: X=', num2str(shoulderRight(1)), ', Y=', num2str(shoulderRight(2)), ...
            ', Z=', num2str(shoulderRight(3))]);

        hold off;
    end
end

% Detener y liberar los objetos de video
stop([colorVid depthVid]);
delete([colorVid depthVid]);