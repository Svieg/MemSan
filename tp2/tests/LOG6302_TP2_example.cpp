class BaseClass {

public:

    int count;

    void* returns_void_pointer() {return 0;}

private:

    long privateAttribute;

};

class ChildClass : public BaseClass {

public:
    int x;

    int bar() {return 0;}

};

class NoMethods_UsesChildClass{

private:

    ChildClass childClassAttribute;

};
