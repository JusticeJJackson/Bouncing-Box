import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.sound.sampled.AudioInputStream;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.Clip;
import javax.sound.sampled.UnsupportedAudioFileException;
import javax.sound.sampled.LineUnavailableException;
import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.File;
import java.io.InputStream;
import java.util.ArrayList;

class Box(double initialY, double initialX, double velocityY, double velocityX, Color color, String soundFile) {
        double yPos = initialY;
        double xPos = initialX;
        double yVelo = velocityY;
        double xVelo = velocityX;
        double boxColor = color;

        try {
        InputStream audioSrc = getClass().getResourceAsStream(soundFile);
        assert audioSrc != null;
        AudioInputStream audioInputStream = AudioSystem.getAudioInputStream(new BufferedInputStream(audioSrc));
        sound = AudioSystem.getClip();
        sound.open(audioInputStream);
        } catch (UnsupportedAudioFileException | IOException | LineUnavailableException e) {
        e.printStackTrace();
        }
        }


class BouncingBoxPanel extends JPanel {
    ArrayList<Box> boxes;
    int boxSize;

    public BouncingBoxPanel(ArrayList<Box> boxes, int boxSize) {
        this.boxes = boxes;
        this.boxSize = boxSize;
        setPreferredSize(new Dimension(70 * boxSize, 50 * boxSize));
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        for (Box box : boxes) {
            g.setColor(box.color);
            g.fillRect((int) (box.xPos * boxSize), (int) (box.yPos * boxSize), boxSize, boxSize);
        }
    }
}

public class BouncingBox {
    public static Box createBox(double initialY, double initialX, double timeInterval, int[] timeSignature, double gridSizeX, double gridSizeY, String soundFile, Color color) {
        double velocityX = ((gridSizeX * 10) / (timeSignature[0])) / (timeInterval * (4.0 / timeSignature[0]));
        double velocityY = (gridSizeY * 10) / (timeInterval * (4.0 / timeSignature[0]));
        return new Box(initialY, initialX, velocityY, velocityX, color, soundFile);
    }

    public static void main(String[] args) {
        ArrayList<Box> boxes = new ArrayList<>();
        boxes.add(createBox(40, 20, 4, new int[]{8, 4}, 70, 50, "\\resources\\3.wav", new Color(255, 255, 0)));
        boxes.add(createBox(0, 0, 4, new int[]{4, 4}, 70, 50, "\\resources\\3.wav", new Color(137, 207, 240)));

        BouncingBoxPanel panel = new BouncingBoxPanel(boxes, 10);

        JFrame frame = new JFrame("Bouncing Box Simulation");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setContentPane(panel);
        frame.pack();
        frame.setResizable(false);
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);

        Timer timer = new Timer(1000 / 60, new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                for (Box box : boxes) {
                    box.xPos += box.xVelo / (1000 / 60);
                    box.yPos += box.yVelo / (1000 / 60);

                    if (box.xPos < 0 || box.xPos > 70 - 1) {
                        box.xVelo = -box.xVelo;
                        box.sound.start();
                    }
                    if (box.yPos < 0 || box.yPos > 50 - 1) {
                        box.yVelo = -box.yVelo;
                        box.sound.start();
                    }
                }
                panel.repaint();
            }
        });
        timer.start();
    }
}

