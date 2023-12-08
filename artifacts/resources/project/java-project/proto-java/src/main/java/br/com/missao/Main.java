package br.com.missao;

import br.com.example.option.AnotherDummy;
import com.google.protobuf.*;
import com.google.protobuf.util.JsonFormat;
import example.complex.ComplexOuterClass;
import example.enumerations.Enumerations;
import example.maps.Maps;
import example.oneofs.Oneofs;
import example.simple.SimpleOuterClass;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.Arrays;
import java.util.Map;
import java.util.concurrent.ExecutionException;

public class Main {

    private static ComplexOuterClass.Dummy createDummy(int id, String name) {
        return ComplexOuterClass.Dummy.newBuilder()
                .setId(id)
                .setName(name)
                .build();
    }

    private static Maps.IdWrapper createIdWrapper(int id) {
        return Maps.IdWrapper.newBuilder()
                .setId(id)
                .build();
    }

    private static void writeTo(SimpleOuterClass.Simple message, String path) {
        try {
            FileOutputStream fs = new FileOutputStream(path);
            message.writeTo(fs);
            fs.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static SimpleOuterClass.Simple readFrom(String path) {
        try {
            FileInputStream fs = new FileInputStream(path);
            SimpleOuterClass.Simple e = SimpleOuterClass.Simple.parseFrom(fs);
            return e;
        } catch (IOException ex) {
            ex.printStackTrace();
        }
        return SimpleOuterClass.Simple.newBuilder().build();
    }

    private static String toJson(SimpleOuterClass.Simple message) throws InvalidProtocolBufferException {
        return JsonFormat.printer().omittingInsignificantWhitespace().print(message);
    }

    private static SimpleOuterClass.Simple fromJson(String data) throws InvalidProtocolBufferException {
        SimpleOuterClass.Simple.Builder builder = SimpleOuterClass.Simple.newBuilder();
        JsonFormat.parser().merge(data, builder);
        return builder.build();
    }

    public static void main(String[] args) throws InvalidProtocolBufferException {
        String path = "Simple.bin";

        // Instantiate a Simple Protobuf Message
        SimpleOuterClass.Simple message = SimpleOuterClass.Simple.newBuilder()
                .setId(42)
                .setIsSimple(true)
                .setName("Tiago Missão")
                .addSampleList(1)
                .addSampleList(2)
                .addSampleList(3)
                .addAllSampleList(Arrays.asList(4,5,6))
                .build();

        System.out.println(message);

        // Write Protobuf to byte file
        Main.writeTo(message, path);

        // Read Protobuf from byte file
        SimpleOuterClass.Simple message2 = Main.readFrom(path);

        // Write Protobuf Json
        String json = Main.toJson(message);
        System.out.println(json);

        SimpleOuterClass.Simple fromJson = Main.fromJson(json);
        System.out.println(fromJson);

        System.out.println(message2);

        // Protobuf with Complex object and repeated fields
        ComplexOuterClass.Complex complex = ComplexOuterClass.Complex.newBuilder()
                .setOneDummy(Main.createDummy(1, "Tiago"))
                .addDummies(Main.createDummy(2, "João"))
                .addDummies(Main.createDummy(3, "Pedro"))
                .addDummies(Main.createDummy(4, "Mateus"))
                .build();

        System.out.println(complex);

        // Protobuf with Enumeration
        Enumerations.EnumerationOrBuilder enumeration = Enumerations.Enumeration.newBuilder()
                .setEyeColor(Enumerations.EyeColor.GREEN)
                .build();

        System.out.println(enumeration);

        // Protobuf with Map
        Maps.MapExample map = Maps.MapExample.newBuilder()
                .putIds("A", Main.createIdWrapper(1))
                .putAllIds(Map.of(
                        "B", Main.createIdWrapper(2),
                        "C", Main.createIdWrapper(3)
                ))
                .build();

        System.out.println(map);

        // Protobuf with OneOf
        Oneofs.Result oneofs1 = Oneofs.Result.newBuilder()
                .setMessage("Hello!")
                .setId(43)
                .build();

        System.out.println("Oneofs1 " + oneofs1);
        System.out.println("Oneofs1 hasMessage " + oneofs1.hasMessage());
        System.out.println("Oneofs1 hasId " + oneofs1.hasId());
        System.out.println("Oneofs1 case " + oneofs1.getResultCase());

        Oneofs.Result oneofs2 = Oneofs.Result.newBuilder()
                .setId(43)
                .setMessage("Hello!")
                .build();

        System.out.println("Oneofs2 " + oneofs2);
        System.out.println("Oneofs2 hasMessage " + oneofs2.hasMessage());
        System.out.println("Oneofs2 hasId " + oneofs2.hasId());
        System.out.println("Oneofs2 case " + oneofs2.getResultCase());

        // Example with Java Options
        AnotherDummy dummyMessage = AnotherDummy.newBuilder().build();
    }
}