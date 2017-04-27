/**
 * Jasmine Farley
 * 3/13/17
 * Foundations of Artificial intelligence
 */

import java.io.BufferedReader;
import java.util.*;
import java.io.*;

public class BabyNames {

    private static String _gender = null;
    private static int _min = 0;
    private static int _max = 0;
    private static int _num = 0;
    private static int _order = 0;
    private static Hashtable<String, String> _chosenLetter = new Hashtable<String, String>();

    private static void markov(String latestName, int markovOrder)
    {
        if(markovOrder==0)
        {
            latestName = "_"+ latestName +"_";
            for(int i=0;i<latestName.length()-1;i++)
            {
                String hashKey=latestName.substring(i, i+1);
                String hashValue=latestName.substring(i+1,i+2);
                letterToChoose(hashKey,hashValue);
            }
        }

        for(int i=0;i<markovOrder;i++)
        {
            latestName = "_" + latestName + "_";
        }

        for(int i=0; i+markovOrder <latestName.length();i++)
        {
            String hashKey = latestName.substring(i, i+markovOrder);
            String hashValue = latestName.substring(i+markovOrder,i+markovOrder+1);
            letterToChoose (hashKey,hashValue);
        }
    }

    private static void letterToChoose(String hashKey, String hashValue){
        if(_chosenLetter.containsKey(hashKey))
        {
            String value = _chosenLetter.get(hashKey);
            value = value + hashValue;
            _chosenLetter.put(hashKey, value);
        }
        else
        {
            _chosenLetter.put(hashKey, hashValue);
        }
    }

    private static void printnames(ArrayList<String> returnedNames)
    {
        System.out.println("Names to consider: ");
        for (String name: returnedNames)
        {
            System.out.println(name);
        }
    }

    @SuppressWarnings("null")
    private static ArrayList<String> markovModel(String gender, int min, int max, int order, int num)
            throws FileNotFoundException, IOException
    {
        HashSet <String> setOfNames=new HashSet<String>();
        if(gender=="female"){
            try (BufferedReader br = new BufferedReader(new FileReader("namesGirls.txt")))
            {
                String line;
                while ((line = br.readLine()) != null)
                {
                    markov(line,order);
                    setOfNames.add(line);
                    line=br.readLine();
                }

            }
        }
        if(gender=="male")
        {
            try (BufferedReader br = new BufferedReader (new FileReader ("namesBoys.txt")))
            {
                String line;
                while ((line = br.readLine()) != null)
                {
                    markov(line,order);
                    setOfNames.add(line);
                    line=br.readLine();
                }
            }
        }
        
        ArrayList<String> generatedNames = new ArrayList<String>();

        int len=0;
        while  (len!=num) {
            String newNameKey = "_";
            for(int i=0;i < order - 1;i++)
            {
                newNameKey = "_" + newNameKey;
            }
            String nameValue = _chosenLetter.get (newNameKey);
            Random randomGen = new Random();
            int randInt = randomGen.nextInt (nameValue.length());
            newNameKey = newNameKey + nameValue.substring(randInt, randInt+1);
            while (!(newNameKey.substring (newNameKey.length()-1)).equals("_"))
            {
                String latestNameValue = _chosenLetter.get (newNameKey.substring(newNameKey.length() -order));
                Random randomGen2 = new Random();
                int randInt2 = randomGen2.nextInt(latestNameValue.length());
                newNameKey= newNameKey + latestNameValue.substring(randInt2, randInt2 + 1);
            }
            String newName = newNameKey.replace("_", "");
            if (!generatedNames.contains(newName) && !setOfNames.contains(newName) &&
                    newName.length() > min && newName.length()<max)
            {
                generatedNames.add(newName);
                len++;
            }
        }
        return generatedNames;
    }



    public static void main(String[] args) throws IOException{

        Scanner input = new Scanner(System.in);  // Reading from System.in
        System.out.print("male or female? :"); //male or female.
        _gender = input.next();
        if(0==(_gender.compareTo("female"))){
            _gender="female";
        }
        else if(0==(_gender.compareTo("male"))){
            _gender="male";
        }
        System.out.print("The minimum name length: "); //The minimum name length
        _min = input.nextInt();
        System.out.print("The maximum name length: "); //The maximum name length
        _max = input.nextInt();
        System.out.print("The order? : ");
        _order = input.nextInt();
        System.out.print("Number of names: "); // The number of names to generate
        _num = input.nextInt();
        input.close();
        ArrayList<String> generatedNames = markovModel(_gender, _min,_max,_order, _num);
        printnames(generatedNames);
    }

}

