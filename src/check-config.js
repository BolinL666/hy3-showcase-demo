const required = ["TOKENHUB_API_KEY"];

const missing = required.filter((name) => !process.env[name]);

if (missing.length > 0) {
  console.error(`Missing environment variables: ${missing.join(", ")}`);
  console.error("Create a .env file from .env.example or export the variables before running the demo.");
  process.exit(1);
}

console.log("Configuration looks ready.");
