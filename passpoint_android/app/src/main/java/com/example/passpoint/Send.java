package com.example.passpoint;

public class Send {

    class Person {
        public String firstName;
        public String middleName;
        public String lastName;
        public byte[] sign;

        public Person(String firstName, String middleName, String lastName, byte[] sign) {
            this.firstName = firstName;
            this.middleName = middleName;
            this.lastName = lastName;
            this.sign = sign;
        }
    }

    public long IdDevice;
    public long place;
    public Person person;

    public Send(long idDevice, long place, String firstName, String middleName, String lastName, byte[] sign) {
        IdDevice = idDevice;
        this.place = place;
        this.person = new Person(firstName, middleName, lastName, sign);
    }
}
