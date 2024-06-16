CREATE TABLE "orders" (
  "id" SERIAL PRIMARY KEY,
  "description" varchar,
  "total_cost" int,
  "serial_number" varchar,
  "created_at" timestamp,
  "directory_id" int,
  "client_id" int,
  "worker_id" int
);

CREATE TABLE "progress" (
  "id" SERIAL PRIMARY KEY,
  "status" varchar,
  "notes" varchar,
  "created_at" timestamp,
  "id_order" int
);

CREATE TABLE "client" (
  "id" SERIAL PRIMARY KEY,
  "first_name" varchar,
  "second_name" varchar,
  "address" varchar,
  "telephone" varchar,
  "created_at" timestamp
);

CREATE TABLE "worker" (
  "id" SERIAL PRIMARY KEY,
  "first_name" varchar,
  "second_name" varchar,
  "telephone" varchar
);

CREATE TABLE "directory" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar,
  "type" varchar
);

ALTER TABLE "order" ADD FOREIGN KEY ("directory_id") REFERENCES "directory" ("id");

ALTER TABLE "progress" ADD FOREIGN KEY ("id_order") REFERENCES "order" ("id");

ALTER TABLE "order" ADD CONSTRAINT "order_client_id_fkey" FOREIGN KEY ("client_id") REFERENCES "client" ("id");

ALTER TABLE "order" ADD CONSTRAINT "order_worker_id_fkey" FOREIGN KEY ("worker_id") REFERENCES "worker" ("id");
