# Backward compat list
Explanation for [`./backward_compat_nested.parquet`](./backward_compat_nested.parquet)

This file was generated using older Parquet libraries to ensure backward compatibility with older writers.

## Generation

`build.sbt`:
```sbt
import sbt.Keys.libraryDependencies

import scala.collection.Seq

ThisBuild / version := "0.1.0-SNAPSHOT"

ThisBuild / scalaVersion := "2.12.20"

lazy val root = (project in file("."))
  .settings(
    name := "generate-parquet",
      libraryDependencies ++= Seq(
      "org.apache.parquet" % "parquet-hadoop" % "1.12.0",
      "org.apache.parquet" % "parquet-common" % "1.12.0",
      "org.apache.parquet" % "parquet-column" % "1.12.0",
      "org.apache.hadoop" % "hadoop-client" % "3.3.1"
    )

  )
```


```scala
import org.apache.parquet.hadoop.ParquetWriter
import org.apache.parquet.hadoop.metadata.CompressionCodecName
import org.apache.parquet.schema._
import org.apache.parquet.schema.PrimitiveType.PrimitiveTypeName._
import org.apache.parquet.schema.Type.Repetition._
import org.apache.parquet.schema.OriginalType._
import org.apache.hadoop.fs.Path
import org.apache.hadoop.conf.Configuration
import org.apache.parquet.example.data.{Group, GroupWriter}
import org.apache.parquet.example.data.simple.SimpleGroupFactory
import org.apache.parquet.hadoop.example.{ExampleParquetWriter, GroupWriteSupport}

object ParquetWriterApp {

  def buildSchema(): MessageType = {
    new MessageType("MySchema",
      // col_1 group
      new GroupType(OPTIONAL, "col_1",
        new PrimitiveType(OPTIONAL, INT64, "col_2"),
        Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_3"),
        new PrimitiveType(OPTIONAL, BINARY, "col_4"),
        Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_5"),
        new PrimitiveType(OPTIONAL, INT32, "col_6"),
        new PrimitiveType(OPTIONAL, BINARY, "col_7"),
        new GroupType(OPTIONAL, "col_8",
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_9")
        ),
        new PrimitiveType(OPTIONAL, BOOLEAN, "col_10"),
        new GroupType(OPTIONAL, "col_11",
          new PrimitiveType(OPTIONAL, BINARY, "col_12")
        ),
        new PrimitiveType(OPTIONAL, BOOLEAN, "col_13"),
        Types.primitive(BINARY, REPEATED).as(ENUM).named("col_14"),
        new GroupType(REPEATED, "col_15",
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_16"),
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_17"),
          new GroupType(OPTIONAL, "col_18",
            new PrimitiveType(OPTIONAL, INT64, "col_19"),
            new PrimitiveType(OPTIONAL, INT32, "col_20")
          )
        )
      ),
      // col_21 group
      new GroupType(OPTIONAL, "col_21",
        new PrimitiveType(OPTIONAL, INT64, "col_22"),
        Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_23"),
        new PrimitiveType(OPTIONAL, BINARY, "col_24"),
        Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_25"),
        new PrimitiveType(OPTIONAL, INT32, "col_26"),
        new PrimitiveType(OPTIONAL, INT32, "col_27"),
        new PrimitiveType(OPTIONAL, BINARY, "col_28"),
        new GroupType(OPTIONAL, "col_29",
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_30")
        ),
        new PrimitiveType(OPTIONAL, BOOLEAN, "col_31"),
        new GroupType(OPTIONAL, "col_32",
          new PrimitiveType(OPTIONAL, BINARY, "col_33")
        ),
        new PrimitiveType(OPTIONAL, BOOLEAN, "col_34"),
        new GroupType(REPEATED, "col_35",
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_36"),
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_37"),
          new GroupType(OPTIONAL, "col_38",
            new PrimitiveType(OPTIONAL, INT64, "col_39"),
            new PrimitiveType(OPTIONAL, INT32, "col_40")
          )
        )
      ),
      // col_41 group
      new GroupType(OPTIONAL, "col_41",
        new GroupType(OPTIONAL, "col_42",
          new PrimitiveType(OPTIONAL, INT64, "col_43"),
          new PrimitiveType(OPTIONAL, INT32, "col_44")
        ),
        new GroupType(OPTIONAL, "col_45",
          new PrimitiveType(OPTIONAL, INT64, "col_46"),
          new PrimitiveType(OPTIONAL, INT32, "col_47")
        )
      ),
      // col_48
      Types.primitive(BINARY, OPTIONAL).as(ENUM).named("col_48"),
      // col_49 group
      new GroupType(OPTIONAL, "col_49",
        new PrimitiveType(OPTIONAL, INT32, "col_50"),
        new PrimitiveType(OPTIONAL, INT64, "col_51"),
        new PrimitiveType(OPTIONAL, FLOAT, "col_52"),
        new PrimitiveType(OPTIONAL, INT32, "col_53"),
        new PrimitiveType(OPTIONAL, INT32, "col_54"),
        new PrimitiveType(OPTIONAL, INT32, "col_55"),
        new PrimitiveType(OPTIONAL, INT64, "col_56"),
        new PrimitiveType(OPTIONAL, INT64, "col_57"),
        Types.primitive(BINARY, OPTIONAL).as(ENUM).named("col_58"),
        new GroupType(OPTIONAL, "col_59",
          new PrimitiveType(OPTIONAL, INT32, "col_60")
        ),
        new GroupType(OPTIONAL, "col_61",
          new PrimitiveType(OPTIONAL, INT32, "col_62")
        ),
        new PrimitiveType(OPTIONAL, DOUBLE, "col_63"),
        new PrimitiveType(OPTIONAL, DOUBLE, "col_64"),
        new PrimitiveType(OPTIONAL, INT32, "col_65")
      ),
      // col_66 group
      new GroupType(OPTIONAL, "col_66",
        new PrimitiveType(OPTIONAL, INT32, "col_67"),
        new PrimitiveType(OPTIONAL, INT64, "col_68"),
        new PrimitiveType(OPTIONAL, FLOAT, "col_69"),
        new PrimitiveType(OPTIONAL, INT32, "col_70"),
        new PrimitiveType(OPTIONAL, INT32, "col_71"),
        new PrimitiveType(OPTIONAL, INT32, "col_72"),
        new PrimitiveType(OPTIONAL, INT64, "col_73"),
        new PrimitiveType(OPTIONAL, INT64, "col_74"),
        Types.primitive(BINARY, OPTIONAL).as(ENUM).named("col_75"),
        new GroupType(OPTIONAL, "col_76",
          new PrimitiveType(OPTIONAL, INT32, "col_77")
        ),
        new GroupType(OPTIONAL, "col_78",
          new PrimitiveType(OPTIONAL, INT32, "col_79")
        ),
        new PrimitiveType(OPTIONAL, DOUBLE, "col_80"),
        new PrimitiveType(OPTIONAL, DOUBLE, "col_81"),
        new PrimitiveType(OPTIONAL, INT32, "col_82")
      ),
      // col_83 group
      new GroupType(OPTIONAL, "col_83",
        new PrimitiveType(OPTIONAL, BOOLEAN, "col_84"),
        new PrimitiveType(OPTIONAL, INT32, "col_85"),
        new PrimitiveType(OPTIONAL, BOOLEAN, "col_86"),
        new PrimitiveType(OPTIONAL, INT32, "col_87"),
        new PrimitiveType(OPTIONAL, BOOLEAN, "col_88"),
        new PrimitiveType(OPTIONAL, INT32, "col_89")
      ),
      // col_90 group
      new GroupType(OPTIONAL, "col_90",
        new PrimitiveType(OPTIONAL, INT64, "col_91"),
        Types.primitive(BINARY, OPTIONAL).as(ENUM).named("col_92"),
        Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_93"),
        new PrimitiveType(OPTIONAL, INT64, "col_94"),
        new PrimitiveType(OPTIONAL, INT64, "col_95"),
        new PrimitiveType(OPTIONAL, INT64, "col_96"),
        new PrimitiveType(OPTIONAL, INT64, "col_97"),
        new GroupType(REPEATED, "col_98",
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_99"),
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_100")
        ),
        new GroupType(OPTIONAL, "col_101",
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_102")
        ),
        new GroupType(OPTIONAL, "col_103",
          new PrimitiveType(OPTIONAL, BINARY, "col_104"),
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_105"),
          new GroupType(OPTIONAL, "col_106",
            Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_107")
          )
        ),
        new GroupType(OPTIONAL, "col_108",
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_109"),
          new PrimitiveType(OPTIONAL, BINARY, "col_110"),
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_111"),
          new GroupType(OPTIONAL, "col_112",
            Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_113")
          )
        ),
        new GroupType(OPTIONAL, "col_114",
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_115"),
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_116")
        ),
        new GroupType(OPTIONAL, "col_117",
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_118")
        ),
        new GroupType(OPTIONAL, "col_119",
          new PrimitiveType(OPTIONAL, INT64, "col_120")
        ),
        new GroupType(OPTIONAL, "col_121",
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_122")
        ),
        new GroupType(OPTIONAL, "col_123",
          new PrimitiveType(OPTIONAL, INT64, "col_124"),
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_125")
        ),
        new GroupType(OPTIONAL, "col_126",
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_127")
        ),
        new GroupType(OPTIONAL, "col_128",
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_129")
        ),
        new GroupType(OPTIONAL, "col_130",
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_131"),
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_132")
        ),
        new GroupType(OPTIONAL, "col_133",
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_134")
        ),
        new GroupType(OPTIONAL, "col_135",
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_136")
        ),
        new GroupType(OPTIONAL, "col_137",
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_138")
        ),
        new GroupType(OPTIONAL, "col_139",
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_140")
        ),
        new GroupType(OPTIONAL, "col_141",
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_142")
        ),
        new GroupType(OPTIONAL, "col_143",
          Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_144")
        ),
        new GroupType(OPTIONAL, "col_145",
          new PrimitiveType(OPTIONAL, INT64, "col_146")
        ),
        new PrimitiveType(OPTIONAL, BOOLEAN, "col_147")
      ),
      // Remaining top-level fields
      new PrimitiveType(OPTIONAL, BOOLEAN, "col_148"),
      Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_149"),
      new PrimitiveType(OPTIONAL, BOOLEAN, "col_150"),
      new GroupType(OPTIONAL, "col_151",
        new PrimitiveType(OPTIONAL, INT64, "col_152"),
        new PrimitiveType(OPTIONAL, INT32, "col_153")
      ),
      new PrimitiveType(OPTIONAL, BOOLEAN, "col_154"),
      new GroupType(OPTIONAL, "col_155",
        Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_156")
      ),
      new GroupType(OPTIONAL, "col_157",
        Types.primitive(BINARY, OPTIONAL).as(UTF8).named("col_158"),
        new PrimitiveType(OPTIONAL, INT32, "col_159")
      ),
      new PrimitiveType(OPTIONAL, BINARY, "col_160"),
      new PrimitiveType(OPTIONAL, BINARY, "col_161"),
      new GroupType(OPTIONAL, "col_162",
        new PrimitiveType(OPTIONAL, INT32, "col_163"),
        new PrimitiveType(OPTIONAL, INT64, "col_164")
      )
    )
  }

  def main(args: Array[String]): Unit = {
    val outputPath = if (args.length > 0) new Path(args(0)) else new Path("output.parquet")
    val schema = buildSchema()
    val conf = new Configuration()
    
    GroupWriteSupport.setSchema(schema, conf)
    
    val writer = ExampleParquetWriter.builder(outputPath)
      .withConf(conf)
      .withCompressionCodec(CompressionCodecName.SNAPPY)
      .withWriteMode(org.apache.parquet.hadoop.ParquetFileWriter.Mode.OVERWRITE)
      .build()

    try {
      val factory = new SimpleGroupFactory(schema)
      
      // Write a minimal record with the problematic schema structure
      // All fields are optional, so we can write an empty or minimal record
      val record = factory.newGroup()
      
      // Write just enough data to create a valid but minimal Parquet file
      // This preserves the schema structure that may cause reading issues
      val col1 = record.addGroup("col_1")
      col1.add("col_2", 1L)
      
      writer.write(record)
      
      println(s"Successfully wrote Parquet file with problematic schema to: ${outputPath}")
      println(s"Schema has ${schema.getFieldCount} top-level fields")
    } finally {
      writer.close()
    }
  }
}
```