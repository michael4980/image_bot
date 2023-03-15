CREATE TABLE "customer" (
  "id" SERIAL PRIMARY KEY,
  "nick" VARCHAR(50) NOT NULL,
  "tg_id" VARCHAR(30) UNIQUE NOT NULL
);

CREATE TABLE "logger" (
  "id" SERIAL PRIMARY KEY,
  "create_date" TIMESTAMP NOT NULL,
  "operation" VARCHAR(20) NOT NULL,
  "size" INTEGER NOT NULL,
  "image_name" VARCHAR(50) NOT NULL,
  "user" INTEGER NOT NULL
);

CREATE INDEX "idx_logger__user" ON "logger" ("user");

ALTER TABLE "logger" ADD CONSTRAINT "fk_logger__user" FOREIGN KEY ("user") REFERENCES "customer" ("id") ON DELETE CASCADE