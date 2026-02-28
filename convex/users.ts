// Convex authentication for GridToDash
import { query, mutation } from "./_generated/server";
import { v } from "convex/values";

// Get all users (for admin)
export const getUsers = query({
  args: {},
  handler: async (ctx) => {
    return await ctx.db.query("users").collect();
  },
});

// Get user by email
export const getUserByEmail = query({
  args: { email: v.string() },
  handler: async (ctx, args) => {
    const users = await ctx.db
      .query("users")
      .withIndex("email", (q) => q.eq("email", args.email))
      .collect();
    return users[0] || null;
  },
});

// Create new user
export const createUser = mutation({
  args: {
    email: v.string(),
    passwordHash: v.string(),
    name: v.string(),
  },
  handler: async (ctx, args) => {
    // Check if user already exists
    const existing = await ctx.db
      .query("users")
      .withIndex("email", (q) => q.eq("email", args.email))
      .collect();
    
    if (existing.length > 0) {
      throw new Error("User already exists");
    }
    
    const userId = await ctx.db.insert("users", {
      email: args.email,
      passwordHash: args.passwordHash,
      name: args.name,
      createdAt: Date.now(),
    });
    
    return userId;
  },
});

// Verify user credentials
export const verifyUser = query({
  args: { email: v.string(), passwordHash: v.string() },
  handler: async (ctx, args) => {
    const users = await ctx.db
      .query("users")
      .withIndex("email", (q) => q.eq("email", args.email))
      .collect();
    
    if (users.length === 0) {
      return null;
    }
    
    const user = users[0];
    if (user.passwordHash === args.passwordHash) {
      return { email: user.email, name: user.name };
    }
    
    return null;
  },
});
