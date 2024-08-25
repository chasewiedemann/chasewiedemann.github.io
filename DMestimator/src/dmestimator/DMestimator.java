/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package dmestimator;


import com.stata.sfi.SFIToolkit;
import com.stata.sfi.Data;
import com.stata.sfi.Macro;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import org.apache.commons.math3.linear.Array2DRowRealMatrix;
import org.apache.commons.math3.linear.ArrayRealVector;
import org.apache.commons.math3.linear.RealMatrix;
import org.apache.commons.math3.linear.RealVector;


/**
 *
 * @author c.j.wiedemann
 */
public class DMestimator {
    
    // Data
    RealVector d;
    RealMatrix expX;
    RealMatrix utilityX;
    RealMatrix utilityFE;
    RealMatrix W;
    RealMatrix WFE;
    int N;
    
    // g Function
    int R;
    boolean useHypercubes;
    RealMatrix Z;
    RealMatrix G;
    
    // Initial Point Estimation
    boolean useMMM;
    ArrayRealVector initialParameter;
    
    // Initial Testing
    boolean useAS;
    int B;
    boolean isModelRejected;
    boolean isSetIdentified;
    
    //Default Values
    static int defaultR = 1;
    static int defaultB = 250;
    static boolean defaultUseHypercubes = false;
    static boolean defaultUseMaxFunction = true;
    static boolean defaultUseMMM = false;
    static boolean defaultUseAS = false;
    
    
    
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
    }
    
    public DMestimator(){
        
        
        // Get Data
        this.d = DataFetch.getd(); // Agents Choices
        this.N = d.getDimension();
        this.expX = DataFetch.getExpX(); // Covariates in Utility Function Agents Make Expectations Over
        this.utilityX = DataFetch.getUtilityX(); // Covariates in Utility Function Agents Do Not Make Expectations Over
        this.utilityFE = DataFetch.getUtilityFE(); // Fixed Effects in Agents Utility Function
        this.W = DataFetch.getW(); // Continuous Instruments Correlated with Agents Expectations
        this.WFE = DataFetch.getWFE(); // Fixed Effect Instruments
        
        // Set up Binary Matrix G from g Function
        this.R = DataFetch.getR(); // Number of Quantiles to Use
        this.useHypercubes = DataFetch.getUseHypercubes(); // Which g Function to Use
        this.Z = concatenateMatrix(this.utilityX,this.W);
        this.G = generateG(this.useHypercubes); // Binary Matrix for Moment Inclusion
        
        // Estimate Initial Point
        this.useMMM = DataFetch.getUseMMM(); // Selects S Function between Max and MMM
        this.initialParameter = estimateInitialParameter();
        
        
        // Test Initial Parameter
        this.useAS = DataFetch.getUseAS(); // Selects Testing Procedure Between 
        this.B = DataFetch.getB();
        this.isModelRejected = isModelRejected();
        
        
        
        
        
        // Create Confidence Set
        
        // Report to Stata
        DMestimator.publish();
        
    }
    
    
    
    RealMatrix concatenateMatrix(RealMatrix X,RealMatrix Y){
        int rows = X.getRowDimension();
        int columns1 = X.getColumnDimension();
        int columns2 = Y.getColumnDimension();

        RealMatrix result = new Array2DRowRealMatrix(rows, columns1 + columns2);

        result.setSubMatrix(X.getData(), 0, 0); // Insert first matrix
        result.setSubMatrix(Y.getData(), 0, columns1); // Insert second matrix

        return result;
    }
    
    RealMatrix generateG(boolean useHypercubes) {
        if (useHypercubes) {
            return gHypercubes(this.Z,this.R);
        } else{
            return gPairwiseRectangles(this.Z,this.R);
        }
}
    
    static RealMatrix gHypercubes(RealMatrix Z, int R){
        // Returns a ((R+1)^K) X N Matrix
        int K = Z.getColumnDimension();
        int P = (int) Math.pow(R+1,K);
        int N = Z.getRowDimension();
        RealMatrix G = new Array2DRowRealMatrix(P,N);
        
       
        
        for (int i = 0; i < P; i++) {
            for (int j = 0; j < N; j++) {
                G.setEntry(i,j,P(i,j,Z,R,K));
            }
        }
        
        return G;
    }
    
    static RealMatrix gPairwiseRectangles(RealMatrix Z, int R){
        
    }
    
    static RealMatrix generatePermutations(int K, int R) {
        int totalPermutations = (int) Math.pow(R+1,K);
        RealMatrix idxMatrix = new Array2DRowRealMatrix(K,totalPermutations);
        for (int i = 0; i < totalPermutations; i++) {
            double[] permutation = new double[K];
            int temp = i;
            for (int j = 0; j < K; j++) {
                permutation[j] = (double) temp % (R+1);
                temp /= (R+1);
            }
            
            idxMatrix.setRow(i,  permutation);
        }
        return idxMatrix;
    }
    
    static int inPartition(int i, int j,  RealMatrix Z, int R, int K){
        
        RealMatrix idxMatrix = generatePermutations(K,R);
        RealMatrix lbMatrix = new Array2DRowRealMatrix(K,R);
        double point = Z.getEntry(i,j);
        
        
        return 
    }

    
    boolean isModelRejected(){
        return true; // 
    }
    
    static class DataFetch{
        
        static ArrayList<RealMatrix> allMatrices = extractAllData();
       
        // Data
        static RealVector getd(){
            return allMatrices.get(0).getColumnVector(0);
        }
        static RealMatrix getExpX(){
            
            return allMatrices.get(1);
        }
        static RealMatrix getUtilityX(){
            return allMatrices.get(2);
        }
        static RealMatrix getUtilityFE(){
            return allMatrices.get(3);
        }
        static RealMatrix getW(){
            return allMatrices.get(4);
        }
        static RealMatrix getWFE(){
            return allMatrices.get(5);
        }
        
        // Numeric
        static int getR(){
            if (useDefault("R")) {
                return defaultR;
            } else{
                return Integer.parseInt(Macro.getLocal("R"));
            }
        }
        static int getB(){
            if (useDefault("B")) {
                return defaultB;
            } else{
                return Integer.parseInt(Macro.getLocal("B"));
            }
        }
        
        // Booleans
        static boolean getUseHypercubes(){
            if (useDefault("useHypercubes")) {
                return defaultUseHypercubes;
            } else{
                return !defaultUseHypercubes;
            }
        }
        static boolean getUseMMM(){
            if (useDefault("useMMM")) {
                return defaultUseMMM;
            } else{
                return !defaultUseMMM;
            }
        }
        static boolean getUseAS(){
            if (useDefault("useAS")) {
                return defaultUseAS;
            } else{
                return !defaultUseAS;
            }
        }
        // Helper Functions
        static boolean useDefault(String str){
            if (Macro.getLocal(str) == null) {
                return true;
            } else{
                return false;
            }
        }
        static ArrayList<RealMatrix> extractAllData(){
            
            RealMatrix stataD = new Array2DRowRealMatrix();
            RealMatrix stataExpX = new Array2DRowRealMatrix();
            RealMatrix stataUtilityX = new Array2DRowRealMatrix();
            RealMatrix stataUtilityFE = new Array2DRowRealMatrix();
            RealMatrix stataW = new Array2DRowRealMatrix();
            RealMatrix stataWFE = new Array2DRowRealMatrix();
        
            int numExpX = Macro.getLocal("expX").split(" ").length;
            int numUtilityX = Macro.getLocal("utilityX").split(" ").length;
            int numUtilityFE = Macro.getLocal("utilityFE").split(" ").length;
            int numW = Macro.getLocal("W").split(" ").length;
            int numWFE = Macro.getLocal("WFE").split(" ").length;
            
            int counter = 0;
            
            for (long obs = Data.getObsParsedIn1(); obs <= Data.getObsParsedIn2(); obs++) {
            if (!Data.isParsedIfTrue(obs)) {
                continue;
            }
           
            int row = Math.toIntExact(obs);
            
            // Extract Covariate d
            double[] drow = {Data.getNum(Data.getVarIndex(Macro.getLocal("d")),row),0};
            stataD.setRow(counter, drow);            

            // Extract expX
            double[] dataRow = new double[numExpX];
            for (int i = 0; i < numExpX; i++) {
                dataRow[i] =  Data.getNum(Data.getVarIndex(Macro.getLocal("x").split(" ")[i]),row);
            }
            stataExpX.setRow(counter, dataRow);
            
            // Extract utilityX
            dataRow = new double[numUtilityX];
            for (int i = 0; i < numUtilityX; i++) {
                dataRow[i] =  Data.getNum(Data.getVarIndex(Macro.getLocal("z").split(" ")[i]),row);
            }
            stataUtilityX.setRow(counter,dataRow);

            // Extract utilityFE
            dataRow = new double[numUtilityFE];
            for (int i = 0; i < numUtilityFE; i++) {
                dataRow[i] =  Data.getNum(Data.getVarIndex(Macro.getLocal("z").split(" ")[i]),row);
            }
            stataUtilityFE.setRow(counter,dataRow);

            // Extract W
            dataRow = new double[numW];
            for (int i = 0; i < numW; i++) {
                dataRow[i] =  Data.getNum(Data.getVarIndex(Macro.getLocal("z").split(" ")[i]),row);
            }
            stataW.setRow(counter,dataRow);

            // Extract WFE
            dataRow = new double[numWFE];
            for (int i = 0; i < numWFE; i++) {
                dataRow[i] =  Data.getNum(Data.getVarIndex(Macro.getLocal("z").split(" ")[i]),row);
            }
            stataWFE.setRow(counter,dataRow);
    
        }
            ArrayList<RealMatrix> out = new ArrayList<>();
            out.add(stataD);
            out.add(stataExpX);
            out.add(stataUtilityX);
            out.add(stataUtilityFE);
            out.add(stataW);
            out.add(stataWFE);
            return out;
                    
        }
}

    
    
}





