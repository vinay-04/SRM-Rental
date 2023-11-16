import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class App extends JFrame {
    static final String JDBC_DRIVER = "com.mysql.cj.jdbc.Driver";
    static final String DB_URL = "jdbc:mysql://localhost:3306/BloodBank";
    static final String USER = "root";
    static final String PASS = "Abdmsdvk#123";

    public App() {
        super("Blood Bank Management System");
        setSize(400, 300);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JTabbedPane tabbedPane = new JTabbedPane();
        JPanel addDonorPanel = new JPanel();
        addDonorPanel.setLayout(null);
        JPanel checkAvailabilityPanel = new JPanel();
        checkAvailabilityPanel.setLayout(null);

        // Add Donor Form
        JLabel nameLabel = new JLabel("Name:");
        nameLabel.setBounds(10, 20, 80, 25);
        addDonorPanel.add(nameLabel);
        JTextField nameText = new JTextField(20);
        nameText.setBounds(100, 20, 165, 25);
        addDonorPanel.add(nameText);

        JLabel bloodGroupLabel = new JLabel("Blood Group:");
        bloodGroupLabel.setBounds(10, 50, 80, 25);
        addDonorPanel.add(bloodGroupLabel);
        JTextField bloodGroupText = new JTextField(20);
        bloodGroupText.setBounds(100, 50, 165, 25);
        addDonorPanel.add(bloodGroupText);

        JButton addButton = new JButton("Add Donor");
        addButton.setBounds(10, 80, 120, 25);
        addDonorPanel.add(addButton);

        JTextArea resultAreaAddDonor = new JTextArea();
        resultAreaAddDonor.setBounds(10, 110, 300, 150);
        addDonorPanel.add(resultAreaAddDonor);

        // Check Availability Form
        JLabel checkBloodGroupLabel = new JLabel("Blood Group:");
        checkBloodGroupLabel.setBounds(10, 20, 80, 25);
        checkAvailabilityPanel.add(checkBloodGroupLabel);

        JTextField checkBloodGroupText = new JTextField(20);
        checkBloodGroupText.setBounds(100, 20, 165, 25);
        checkAvailabilityPanel.add(checkBloodGroupText);

        JButton checkButton = new JButton("Check Availability");
        checkButton.setBounds(10, 50, 150, 25);
        checkAvailabilityPanel.add(checkButton);

        JTextArea resultArea = new JTextArea();
        resultArea.setBounds(10, 80, 300, 150);
        checkAvailabilityPanel.add(resultArea);

        addButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String name = nameText.getText();
                String bloodGroup = bloodGroupText.getText();
                addDonor(name, bloodGroup, resultAreaAddDonor);
            }
        });

        checkButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String bloodGroup = checkBloodGroupText.getText();
                checkBloodAvailability(bloodGroup, resultArea);
            }
        });

        tabbedPane.addTab("Add Donor", addDonorPanel);
        tabbedPane.addTab("Check Availability", checkAvailabilityPanel);

        add(tabbedPane);
        setVisible(true);
    }

    private void addDonor(String name, String bloodGroup, JTextArea resultAreaAddDonor) {
        Connection conn = null;
        PreparedStatement pstmt = null;
        try {
            Class.forName(JDBC_DRIVER);
            conn = DriverManager.getConnection(DB_URL, USER, PASS);
            String sql = "INSERT INTO Donors (name, blood_group) VALUES (?, ?)";
            pstmt = conn.prepareStatement(sql);
            pstmt.setString(1, name);
            pstmt.setString(2, bloodGroup);
            int rowsInserted = pstmt.executeUpdate();
            if (rowsInserted > 0) {
                resultAreaAddDonor.append("Donor added successfully!");
                resultAreaAddDonor.append("\nName: " + name);
                resultAreaAddDonor.append("\nBloog Group: " + bloodGroup);
                System.out.println("A new donor was added successfully!");
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        } finally {
            try {
                if (pstmt != null)
                    pstmt.close();
                if (conn != null)
                    conn.close();
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        }
    }

    private void checkBloodAvailability(String bloodGroup, JTextArea resultArea) {
        Connection conn = null;
        PreparedStatement pstmt = null;
        ResultSet rs = null;
        try {
            Class.forName(JDBC_DRIVER);
            conn = DriverManager.getConnection(DB_URL, USER, PASS);
            String sql = "SELECT name FROM Donors WHERE blood_group = ?";
            pstmt = conn.prepareStatement(sql);
            pstmt.setString(1, bloodGroup);
            rs = pstmt.executeQuery();
            resultArea.setText("");
            while (rs.next()) {
                String name = rs.getString("name");
                resultArea.append("Name: " + name + "\n");
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        } finally {
            try {
                if (rs != null)
                    rs.close();
                if (pstmt != null)
                    pstmt.close();
                if (conn != null)
                    conn.close();
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new App());
    }
}
