#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define epoca 300000
#define K 0.03f

typedef struct
{
    float Pesos[2];
    float bias;
} Neurona;


//Funcion de Entrenamiento Perceptron
float EntNt(Neurona *, float, float, float);

//Funcion para obtener la salida
float InitNt(Neurona *, float, float);

//Funcion para entrenar la red
void EntrenarRed(Neurona *, Neurona *, Neurona *);

//Funcion para mostrar los resultados
void Resultados(Neurona *, Neurona *, Neurona *);

//Sigmoide
float sigmoide(float);

//pesos aleatorios
void pesos_initNt(Neurona *);


float EntNt(Neurona *n, float x0, float x1, float target)
{
    float net = 0;
    float out = 0;
    float Error;
    float delta[2];

    net = n->Pesos[0]*x0 + n->Pesos[1]*x1 - n->bias;

    net = sigmoide(net);

    Error = target - net;

    n->bias -= K*Error;

    delta[0] = K*Error*x0;
    delta[1] = K*Error*x1;

    n->Pesos[0] += delta[0];
    n->Pesos[1] += delta[1];

    out = net;

    return out;
}


float InitNt(Neurona *n, float x0, float x1)
{
    float net = 0;
    float out = 0;

    net = n->Pesos[0]*x0 + n->Pesos[1]*x1 - n->bias;

    net = sigmoide(net);

    out = net;

    return out;
}


void EntrenarRed(Neurona *AND, Neurona *OR, Neurona *XOR)
{
    float entradas[4][2] =
    {
        {1,1},
        {1,0},
        {0,1},
        {0,0}
    };

    float targetAND[4] = {1,0,0,0};
    float targetOR[4] = {1,1,1,0};
    float targetXOR[4] = {0,1,1,0};

    float salidaAND;
    float salidaOR;

    int i;
    int j;


    for(i = 0; i < epoca; i++)
    {
        for(j = 0; j < 4; j++)
        {
            //Primera capa
            EntNt(
                AND,
                entradas[j][0],
                entradas[j][1],
                targetAND[j]
            );

            EntNt(
                OR,
                entradas[j][0],
                entradas[j][1],
                targetOR[j]
            );


            //Se obtienen las salidas de AND y OR
            salidaAND = InitNt(
                AND,
                entradas[j][0],
                entradas[j][1]
            );

            salidaOR = InitNt(
                OR,
                entradas[j][0],
                entradas[j][1]
            );


            //Las salidas anteriores entran a XOR
            EntNt(
                XOR,
                salidaAND,
                salidaOR,
                targetXOR[j]
            );
        }
    }
}


void Resultados(Neurona *AND, Neurona *OR, Neurona *XOR)
{
    float entradas[4][2] =
    {
        {1,1},
        {1,0},
        {0,1},
        {0,0}
    };

    float salidaAND;
    float salidaOR;
    float apr;

    int i;


    printf("------------------------\n");
    printf("Resultados despues de %d epocas\n", epoca);

    for(i = 0; i < 4; i++)
    {
        salidaAND = InitNt(
            AND,
            entradas[i][0],
            entradas[i][1]
        );

        salidaOR = InitNt(
            OR,
            entradas[i][0],
            entradas[i][1]
        );

        apr = InitNt(
            XOR,
            salidaAND,
            salidaOR
        );

        printf("%.0f,%.0f=%f\n",
               entradas[i][0],
               entradas[i][1],
               apr);
    }

    printf("\n");

    printf("Pesos XOR\n");
    printf("Peso 0 = %f\n", XOR->Pesos[0]);
    printf("Peso 1 = %f\n", XOR->Pesos[1]);
    printf("Bias = %f\n", XOR->bias);

    printf("------------------------\n");
}


void pesos_initNt(Neurona *n)
{
    int i;

    for(i = 0; i < 2; i++)
    {
        n->Pesos[i] = (float)rand()/RAND_MAX;
    }

    n->bias = 0.5f;
}


float sigmoide(float s)
{
    return (1/(1 + expf(-s)));
}


int main()
{
    Neurona AND;
    Neurona OR;
    Neurona XOR;

    //Se inicializan las tres neuronas
    pesos_initNt(&AND);
    pesos_initNt(&OR);
    pesos_initNt(&XOR);


    /*
        La solucion utiliza AND y OR como capa oculta.
        Las salidas de estas dos neuronas se utilizan
        como entradas para la neurona que obtiene XOR.
    */

    EntrenarRed(&AND, &OR, &XOR);

    Resultados(&AND, &OR, &XOR);

    return 0;
}
