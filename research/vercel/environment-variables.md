# Vercel Environment Variables Guide

## Definition
"Environment variables are key-value pairs configured outside your source code so that each value can change depending on the Environment."

## Key Characteristics
- **Encrypted at rest**: Secure storage of sensitive data
- **Visible to project users**: Team members can view variables
- **Flexible usage**: Can contain both non-sensitive and sensitive data
- **Build and runtime access**: Usable during build steps and function execution

## Environment Types

### 1. Production
Variables used in production deployments

### 2. Preview
Variables used in preview deployments (pull requests)

### 3. Development
Variables used in local development

### 4. Custom Environments
Create custom environments for specific needs

## Setting Environment Variables

### Dashboard Method
1. Navigate to Project Settings
2. Select "Environment Variables" tab
3. Add key-value pairs
4. Select target environments
5. Save changes

### CLI Method
```bash
# Add a variable
vercel env add

# Add with specific value
vercel env add API_KEY production

# Add to multiple environments
vercel env add DATABASE_URL production preview
```

### Configuration Levels

#### Team-Level Variables
- Apply to all projects within a team
- Useful for shared configuration
- Can be overridden at project level

#### Project-Level Variables
- Specific to individual projects
- Override team-level variables
- Most common configuration method

## Size Limitations

### General Limits
- **64 KB total** per deployment
- Includes all environment variables combined

### Edge Functions and Middleware
- **5 KB per variable** maximum
- More restrictive due to edge runtime constraints

### Calculating Size
```javascript
// Example calculation
const envSize = Object.entries(process.env)
  .reduce((total, [key, value]) => {
    return total + key.length + value.length + 2; // +2 for = and newline
  }, 0);

console.log(`Total env size: ${envSize} bytes`);
```

## Access Methods

### Local Development
```bash
# Pull environment variables to local file
vercel env pull .env.local

# Creates .env.local with development variables
```

### Build Time Access
```javascript
// Next.js example
module.exports = {
  env: {
    API_URL: process.env.API_URL,
  },
}
```

### Runtime Access
```javascript
// Server-side code
const apiKey = process.env.API_KEY;

// Client-side (Next.js)
const publicKey = process.env.NEXT_PUBLIC_API_KEY;
```

## Best Practices

### 1. Naming Conventions
```bash
# Public variables (Next.js)
NEXT_PUBLIC_API_URL=https://api.example.com

# Private variables
DATABASE_URL=postgresql://...
API_SECRET=secret_key_here
```

### 2. Security
- Never commit `.env` files to version control
- Use different values for different environments
- Rotate secrets regularly
- Limit access to sensitive variables

### 3. Organization
```bash
# Group related variables
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp

# External APIs
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# Feature flags
ENABLE_BETA_FEATURES=true
```

## Supported Runtimes

### Node.js
```javascript
// Access all variables through process.env
const apiUrl = process.env.API_URL;
```

### Python
```python
import os
api_url = os.environ.get('API_URL')
```

### Ruby
```ruby
api_url = ENV['API_URL']
```

### Go
```go
apiUrl := os.Getenv("API_URL")
```

### PHP (Community Runtime)
```php
$apiUrl = $_ENV['API_URL'];
```

### Custom Runtimes
Via Build Output API - consult specific runtime documentation

## Common Patterns

### Development vs Production
```javascript
// Use different values per environment
const apiUrl = process.env.NODE_ENV === 'production'
  ? process.env.PROD_API_URL
  : process.env.DEV_API_URL;
```

### Required Variables
```javascript
// Validate required variables
const requiredEnvVars = ['DATABASE_URL', 'API_KEY'];

requiredEnvVars.forEach(varName => {
  if (!process.env[varName]) {
    throw new Error(`Missing required environment variable: ${varName}`);
  }
});
```

### Type Conversion
```javascript
// Convert string to number
const port = parseInt(process.env.PORT || '3000', 10);

// Convert to boolean
const isDebug = process.env.DEBUG === 'true';
```

## Debugging

### List Variables
```bash
# List all environment variables
vercel env ls

# List for specific environment
vercel env ls production
```

### Verify in Deployment
```javascript
// Log environment (careful with sensitive data!)
console.log('Environment:', process.env.NODE_ENV);
console.log('API URL:', process.env.API_URL);
```

## Important Notes

1. **Changes require redeployment**: Environment variable changes only apply to new deployments
2. **Build vs Runtime**: Some variables are only available at build time
3. **Case sensitive**: Variable names are case-sensitive
4. **No interpolation**: Variables don't support interpolation (e.g., `$OTHER_VAR` won't expand)

## Example Configuration

```bash
# .env.local (development)
DATABASE_URL=postgresql://localhost:5432/dev
API_KEY=dev_key_12345
NEXT_PUBLIC_API_URL=http://localhost:3001

# Production (via Vercel Dashboard)
DATABASE_URL=postgresql://prod-server:5432/prod
API_KEY=prod_key_secure_67890
NEXT_PUBLIC_API_URL=https://api.myapp.com
```

## Migration from Other Platforms
When migrating from other platforms, ensure:
1. All required variables are configured
2. Variable names match your code expectations
3. Secrets are properly encrypted
4. Environment-specific values are set correctly

For detailed implementation guidance, refer to Vercel's "Managing environment variables" documentation.