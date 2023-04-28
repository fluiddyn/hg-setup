FoamFile
{
    version     2.0;
    format      ascii;
    class       volVectorField;
    object      Ub;
}

dimensions  [0 1 -1 0 0 0 0];

internalField   uniform (0 0 0);

boundaryField
{
    inlet
    {
        type            cyclic;
    }
    outlet
    {
        type            cyclic;
    }
    top
    {
        type            zeroGradient;
    }
    bottom
    {
        type            fixedValue;
        value           uniform (0 0 0);
    }
    frontAndBackPlanes
    {
        type            empty;
    }
}
