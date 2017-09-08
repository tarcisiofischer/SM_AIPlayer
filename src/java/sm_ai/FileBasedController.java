package sm_ai;

import java.io.IOException;
import java.io.PrintWriter;

public class FileBasedController implements Controller {

    private PrintWriter writer;
    private boolean _state[];

	public FileBasedController() {
		_state = new boolean[Button.values().length];
        for (int i = 0; i < _state.length; i++) {
            _state[i] = false;
        }

        try{
    	    writer = new PrintWriter("/tmp/action.txt", "UTF-8");
		} catch (IOException e) {}
	}

	@Override
	public void press(Button b) {
		_state[b.getValue()] = true;
		update_keys();
	}

	@Override
	public void release(Button b) {
		_state[b.getValue()] = false;
		update_keys();
	}
	
	private void update_keys() {
		for (boolean button_state : _state) {
			if (button_state) {
	    	    writer.println("1");
			} else {
	    	    writer.println("0");
			}
		}
	}
}
