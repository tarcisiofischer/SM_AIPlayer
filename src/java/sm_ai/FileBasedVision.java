package sm_ai;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.Scanner;

public class FileBasedVision implements Vision {

	@Override
	public int[] mario_position() {
		int x = 0;
		int y = 0;
		try {
			BufferedReader br = new BufferedReader(new FileReader("/tmp/vision.txt"));
			String line = br.readLine();
			String[] values = line.split(",");
			x = Integer.parseInt(values[1].trim());
			y = Integer.parseInt(values[0].trim());
			br.close();
		} catch (IOException e) {
			e.printStackTrace();			
		}
		
		return new int[]{x, y};
	}

	@Override
	public int[] block_position() {
		int x = 0;
		int y = 0;
		try {
			BufferedReader br = new BufferedReader(new FileReader("/tmp/vision.txt"));
			br.readLine(); // Ignore first line

			String line = br.readLine();
			String[] values = line.split(",");
			x = Integer.parseInt(values[1].trim());
			y = Integer.parseInt(values[0].trim());
			br.close();
		} catch (IOException e) {
			e.printStackTrace();			
		}
		
		return new int[]{x, y};
	}
}
