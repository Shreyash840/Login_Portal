schema_for_post = {
  "type": "object",
  "properties": {
    "username": {
      "type": "string"
    },
    "password": {
      "type": "string"
    },
    "email": {
      "type": "string"
    }
  },
  "required": [
    "username",
    "password",
    "email"
  ]
}
schema_for_put = {
  "type": "object",
  "properties": {
    "username": {
      "type": "string"
    },
    "password": {
      "type": "string"
    }
  },
  "required": [
    "username",
    "password"
  ]
}