package sm_ai;

public interface Controller {
	enum Button {
		LEFT(0),
		RIGHT(1),
		UP(2),
		DOWN(3),
		JUMP(4);
		
	    private final int value;
	    private Button(int value) {
	        this.value = value;
	    }

	    public int getValue() {
	        return value;
	    }
	}
	
	void press(Button b);
	void release(Button b);
}
