import java.util.Arrays;
import java.util.Random;

public class readerClass {
	
	public static void main(String[] args) {
//		String sess = "bambambam";
//		String[] ses = sess.split("");
//		System.out.println(Arrays.toString(ses));
//		Random random = new Random();
//		System.out.println(random.nextInt(2));
		String input1 = "spaghetti";
		int slice = 0;
		System.out.println(input1);
		for (int i = 3; i >= 0; i--) {
			String s = input1.substring(slice,i);
			System.out.println(s);
	}
	}
}
