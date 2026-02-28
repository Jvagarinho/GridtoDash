// Convex schema for GridToDash users
import { defineSchema, defineTable } from "convex/server";
import { auth } from "./auth";

export default defineSchema({
  users: defineTable({
    email: "string",
    passwordHash: "string",
    name: "string",
    createdAt: "number",
  }).index("email", ["email"]),
});
