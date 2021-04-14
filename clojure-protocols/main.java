public interface Dog {
    public void bark();
    public void bark(int x);
    public void eat();
}

public interface Playful {
    public void play();
}

public class Pitbull implements Dog, Playful {
    private String name;

    public Pitbull(String name) {
        this.name = name;
    }

    public void bark() {
        System.out.println(this.name + " goes 'RRRooof! Woof woof!'");
    }

    public void bark(int x) {
        for (int i = 0; i < x; i++) {
            bark();
        }
    }

    public void eat() {
        System.out.println(this.name + " eats and grunts");
    }

    public void play() {
        System.out.println(this.name + " is chasing the ball");
    }
}