package com.cats;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) throws IOException {

        System.out.println("Что вы хотите сделать?\n1. Зашифровать файл\n2. Расшифровать файл\n->");
        Scanner scanner = new Scanner(System.in);
        String commandInput = scanner.next();
        System.out.println(commandInput);

        //Шифрование файла
        if (commandInput.equals("1")) {
            System.out.println("Введите путь к файлу для его шифрования");

            String file2EncryptString = scanner.next();
            if (!IsFileExists(file2EncryptString)) {
                System.out.println("Введенного файла не существует");
                return;
            }
            FileProcessing inputFile = new FileProcessing(file2EncryptString);

            //Генерируем ключ шифрования
            byte[] keyBytes = KeyGenerator();
            AESClass obj = new AESClass(keyBytes);
            byte[] encrypt = obj.Encrypt(inputFile.Read());

            //Запись ключа
            FileProcessing outputKeyFile = new FileProcessing(GetKeyDirByPath(file2EncryptString));
            outputKeyFile.Write(keyBytes);
            //Запись зашифрованного файла на место предыдущего
            FileProcessing outputDataFile = new FileProcessing(file2EncryptString);
            outputDataFile.Write(encrypt);

            System.out.println("Успешно зашифровали файл " + file2EncryptString);
        }

        //Расшифровка файла
        else if (commandInput.equals("2")) {

            System.out.println("Введите путь к файлу для его расшифровки");
            String file2DecryptString = scanner.next();
            if (!IsFileExists(file2DecryptString)) {
                System.out.println("Введенного файла не существует");
                return;
            }
            System.out.println("Введите путь к файлу-ключу для расшифровки");
            String DecryptKeyString = scanner.next();
            if (!IsFileExists(DecryptKeyString)) {
                System.out.println("Введенного файла не существует");
                return;
            }

            FileProcessing inputKeyObj = new FileProcessing(DecryptKeyString);
            FileProcessing inputFileObj = new FileProcessing(file2DecryptString);

            AESClass obj = new AESClass(inputKeyObj.Read());
            byte[] decrypt = obj.Decrypt(inputFileObj.Read());

            FileProcessing resultDataFile = new FileProcessing(file2DecryptString);
            resultDataFile.Write(decrypt);

            System.out.println("Успешно расшифровали файл");

        }
        else
            System.out.println("Некорректный ввод данных..");
    }

    //Генерирует ключ для шифрования данных
    private static byte[] KeyGenerator() {
        StringBuilder key = new StringBuilder();
        for (int i = 0; i < 2; i++)
            key.append(Long.toHexString(Double.doubleToLongBits(Math.random())));
        return key.toString().getBytes();
    }

    //Проверка на существование файла из строки
    private static boolean IsFileExists(String Path) {
        File tempFile = new File(Path);
        return tempFile.exists();
    }

    //Получение названия файла-ключа на основе названия файла-источника
    private static String GetKeyDirByPath(String dir){

        //Значит это директория UNIX-подобная
        if (dir.contains("/")) {
            String[] bufArr = dir.split("/");
            String filename = bufArr[bufArr.length-1].split("\\.")[0];
            String keyName = filename+"_key.cat";
            bufArr = Arrays.copyOf(bufArr, bufArr.length-1);
            return String.join("/", bufArr)+"/"+keyName;
        }
        //Значит это винда
        else if (dir.contains("\\")){
            String[] bufArr = dir.split("\\\\");
            String filename = bufArr[bufArr.length-1].split("\\.")[0];
            String keyName = filename+"_key.cat";
            bufArr = Arrays.copyOf(bufArr, bufArr.length-1);
            return String.join("\\", bufArr)+"\\"+keyName;
        }
        else {
            String filename = dir.split("\\.")[0];
            return filename+"_key.cat";

        }

    }

}
