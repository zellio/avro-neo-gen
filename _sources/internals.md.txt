# Internals

## Lexer

```{eval-rst}
.. automodule:: avro_neo_gen.lexer
    :members: read_path
```

## Parser

```{eval-rst}
.. automodule:: avro_neo_gen.parser
    :members: parse_schema
```

## Compiler

```{eval-rst}
.. automodule:: avro_neo_gen.compiler
    :members:
        compile_avro_schema,
        compile_avro_schema_record_body,
        compile_avro_schema_record_builder,
        compile_avro_schema_type_signature,
        compile_parser_namespace_map,
```

## Linker

```{eval-rst}
.. automodule:: avro_neo_gen.linker
    :members:
        avro_schema_required_imports,
        emit_linker_file_map,
        inject_corelib_sys_path_shim,
        link_compiler_namespace_map,
        link_corelib,
        link_module,
```

## Classes

```{eval-rst}
.. autoclass:: avro_neo_gen.avro_schema.AvroSchema
    :show-inheritance:
    :members:
    :special-members: __getattr__, __eq__, __iter__
```

## Type Defs

```{eval-rst}
.. autoclass:: avro_neo_gen.type_defs.CompilerNamespaceMapCell
    :show-inheritance:
    :members:
```

```{eval-rst}
.. automodule:: avro_neo_gen.type_defs
    :members:
        ParserNamespaceMap,
        CompilerNamespaceMap,
        ModuleImports,
        LinkerRequiredImports,
        LinkerFileMap,
```
