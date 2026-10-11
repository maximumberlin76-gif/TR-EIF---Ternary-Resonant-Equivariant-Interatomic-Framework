{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "TR-EIF Observable Bundle",
  "description": "Structural JSON schema for the physical observable bundle associated with one TR-EIF execution state. Energy, forces, and stress remain continuous physical observables and are structurally distinct from balanced-ternary execution state.",
  "type": "object",
  "required": [
    "node_count",
    "energy",
    "forces",
    "stress"
  ],
  "additionalProperties": false,
  "properties": {
    "node_count": {
      "type": "integer",
      "minimum": 1,
      "description": "Number of represented execution or atomic nodes."
    },
    "energy": {
      "oneOf": [
        {
          "type": "null"
        },
        {
          "$ref": "energy_output.schema.json"
        }
      ],
      "description": "Optional conservative energy observable. JSON null represents absence of this observable and is not encoded as ternary state 0."
    },
    "forces": {
      "oneOf": [
        {
          "type": "null"
        },
        {
          "$ref": "#/$defs/force_state"
        }
      ],
      "description": "Optional Cartesian force observable. JSON null represents absence of this observable and is not encoded as ternary state 0."
    },
    "stress": {
      "oneOf": [
        {
          "type": "null"
        },
        {
          "$ref": "#/$defs/stress_state"
        }
      ],
      "description": "Optional Cartesian stress observable. JSON null represents absence of this observable and is not encoded as ternary state 0."
    }
  },
  "$defs": {
    "vector3": {
      "type": "array",
      "minItems": 3,
      "maxItems": 3,
      "items": {
        "type": "number"
      }
    },
    "tensor3x3": {
      "type": "array",
      "minItems": 3,
      "maxItems": 3,
      "items": {
        "$ref": "#/$defs/vector3"
      }
    },
    "force_state": {
      "type": "object",
      "required": [
        "forces"
      ],
      "additionalProperties": false,
      "properties": {
        "forces": {
          "type": "array",
          "minItems": 1,
          "items": {
            "$ref": "#/$defs/vector3"
          },
          "description": "Ordered Cartesian force vectors, one vector per represented atom."
        }
      }
    },
    "stress_state": {
      "type": "object",
      "required": [
        "tensor"
      ],
      "additionalProperties": false,
      "properties": {
        "tensor": {
          "$ref": "#/$defs/tensor3x3",
          "description": "Cartesian 3x3 stress tensor under the currently declared TR-EIF stress convention."
        }
      }
    }
  },
  "$comment": "TR-EIF observable semantics preserve strict layer separation. Energy is not ternary state. Force is not ternary state. Stress is not ternary state. Ternary state is not energy or force. Missing observables are represented by JSON null, never by active neutral state 0. Runtime TraceRecord invariants additionally enforce energy and force atom counts equal to node_count and finite numeric values. Stress convention and force = -dE/dr remain executable/model contracts rather than properties inferred by this structural schema."
}
