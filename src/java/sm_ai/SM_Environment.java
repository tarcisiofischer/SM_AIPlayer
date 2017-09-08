package sm_ai;
import jason.asSyntax.*;
import jason.environment.Environment;
import sm_ai.Controller.Button;

import java.util.logging.Logger;

public class SM_Environment extends Environment {
    private Player _agent;

    @Override
    public void init(String[] args) {
    	_agent = new Player();
    }
    
    @Override
    public boolean executeAction(String ag, Structure action) {
    	_agent.processAction(action);
        return true;
    }

    private class Player {
        private final Term press_right = Literal.parseLiteral("press(right)");
        private final Term press_jump = Literal.parseLiteral("press(jump)");
        private final Term release_jump = Literal.parseLiteral("release(jump)");

        private Controller _controller;
        private Thread _perception_thread;
        private SM_Environment environment;

    	public Player() {
        	_controller = new FileBasedController();

        	_perception_thread = new Thread(new PerceptionHandler(this));
        	_perception_thread.start();
        }

    	public void processAction(Structure action) {
        	if (action.equals(press_right)) {
            	_controller.press(Button.RIGHT);
            } else if (action.equals(press_jump)) {
            	_controller.press(Button.JUMP);
            } else if (action.equals(release_jump)) {
            	_controller.release(Button.JUMP);
            }
    	}

		private class PerceptionHandler implements Runnable {
			private Player self;
			private boolean __tmp;
			
			public PerceptionHandler(Player p) {
				self = p;
				__tmp = false;
			}
			
			public void run() {
				while (true) {
//					if (__tmp) {
//					self.environment.addPercept(Literal.parseLiteral("something(blocking_passage)"));
//					} else {
//						self.environment.addPercept(Literal.parseLiteral("nothing(blocking_passage)"));
//					}
					__tmp = !__tmp;

					try {
						Thread.sleep(1000);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
				}
			}
		}

    }
}
