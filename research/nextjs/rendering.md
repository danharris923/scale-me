# Next.js: Rendering Guide - Partial Prerendering (PPR)

## Overview
Partial Prerendering is an experimental rendering approach in Next.js that combines static and dynamic content in the same route, providing optimal performance while supporting personalized content.

## Key Concepts

### Rendering Strategies

#### 1. Static Rendering
- HTML generated ahead of time (at build time)
- Cached and shared across users and requests
- Creates a "static shell" for a route
- Best for content that doesn't change frequently

```typescript
// This component will be statically rendered
export default function StaticComponent() {
  return (
    <div>
      <h1>Welcome to our site</h1>
      <p>This content is the same for all users</p>
    </div>
  )
}
```

#### 2. Dynamic Rendering
- HTML generated at request time
- Allows personalized content based on request-time data
- Triggered by using specific APIs:
  - `cookies()`
  - `headers()`
  - `searchParams`
  - `fetch()` with `{ cache: 'no-store' }`

```typescript
import { cookies } from 'next/headers'

// This component will be dynamically rendered
export default async function DynamicComponent() {
  const cookieStore = cookies()
  const theme = cookieStore.get('theme')
  
  return (
    <div>
      <h1>Welcome back!</h1>
      <p>Your theme preference: {theme?.value || 'light'}</p>
    </div>
  )
}
```

## Partial Prerendering (PPR)

### Key Components

#### Suspense Boundaries
Used to mark "dynamic boundaries" in the component tree:

```typescript
import { Suspense } from 'react'

export default function Page() {
  return (
    <div>
      {/* Static content - rendered at build time */}
      <header>
        <h1>My Application</h1>
      </header>
      
      {/* Dynamic content - rendered at request time */}
      <Suspense fallback={<LoadingSkeleton />}>
        <DynamicUserContent />
      </Suspense>
      
      {/* More static content */}
      <footer>
        <p>© 2024 My Company</p>
      </footer>
    </div>
  )
}
```

#### Streaming
Splits route into chunks and progressively streams to client:
- Static shell is sent immediately
- Dynamic content streams in as it becomes ready
- Improves Time to First Byte (TTFB) and First Contentful Paint (FCP)

### Enabling PPR

1. **Configure Next.js**:
```typescript
// next.config.ts
import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  experimental: {
    ppr: 'incremental', // Enable PPR incrementally
  },
}

export default nextConfig
```

2. **Enable for Specific Routes**:
```typescript
// app/posts/page.tsx
export const experimental_ppr = true

export default function PostsPage() {
  return (
    <>
      {/* Static header */}
      <h1>Blog Posts</h1>
      
      {/* Dynamic content with Suspense */}
      <Suspense fallback={<PostsLoading />}>
        <PostsList />
      </Suspense>
    </>
  )
}
```

### Complete PPR Example

```typescript
// app/dashboard/page.tsx
export const experimental_ppr = true

import { Suspense } from 'react'
import { 
  StaticHeader, 
  UserProfile, 
  RecentActivity, 
  Recommendations 
} from '@/components/dashboard'

export default function DashboardPage() {
  return (
    <div className="dashboard">
      {/* Static content - cached and shared */}
      <StaticHeader />
      
      <div className="grid grid-cols-3 gap-4">
        {/* Dynamic user-specific content */}
        <Suspense fallback={<div>Loading profile...</div>}>
          <UserProfile />
        </Suspense>
        
        {/* Dynamic activity feed */}
        <Suspense fallback={<div>Loading activity...</div>}>
          <RecentActivity />
        </Suspense>
        
        {/* Dynamic recommendations */}
        <Suspense fallback={<div>Loading recommendations...</div>}>
          <Recommendations />
        </Suspense>
      </div>
      
      {/* Static footer */}
      <footer>Static footer content</footer>
    </div>
  )
}

// Components
async function UserProfile() {
  const user = await getCurrentUser() // Uses cookies/auth
  return <div>Welcome, {user.name}!</div>
}

async function RecentActivity() {
  const activity = await getUserActivity() // Personalized data
  return (
    <ul>
      {activity.map(item => (
        <li key={item.id}>{item.description}</li>
      ))}
    </ul>
  )
}
```

### Benefits of PPR

1. **Improved Initial Page Performance**
   - Static shell loads instantly
   - Dynamic content streams in progressively

2. **Personalization Support**
   - Dynamic sections can show user-specific content
   - No compromise on caching efficiency

3. **SEO Benefits**
   - Static content is immediately available to crawlers
   - Dynamic content enhances user experience

4. **Developer Experience**
   - Clear separation of static and dynamic content
   - Granular control over rendering behavior

### Best Practices

1. **Identify Static vs Dynamic Content**
   ```typescript
   // Static: Navigation, headers, footers, marketing content
   <Navigation />
   
   // Dynamic: User data, real-time info, personalized content
   <Suspense fallback={<Skeleton />}>
     <UserDashboard />
   </Suspense>
   ```

2. **Use Appropriate Fallbacks**
   ```typescript
   <Suspense fallback={<ContentSkeleton />}>
     <DynamicContent />
   </Suspense>
   ```

3. **Optimize Suspense Boundaries**
   - Don't wrap entire page in Suspense
   - Create boundaries around specific dynamic sections
   - Keep static content outside Suspense

4. **Monitor Performance**
   - Use Next.js Analytics to track improvements
   - Monitor Core Web Vitals
   - Test with real user scenarios

### When to Use PPR

✅ **Good Use Cases:**
- E-commerce product pages (static product info + dynamic inventory)
- News sites (static article + dynamic comments)
- Dashboard pages (static layout + dynamic data)
- Marketing pages with personalization

❌ **Avoid PPR When:**
- Page is entirely static
- Page is entirely dynamic
- Content updates very frequently
- Real-time requirements (use client-side rendering)

## Summary
Partial Prerendering combines the best of static and dynamic rendering, providing fast initial loads while supporting personalized, dynamic content. It's especially powerful for applications that need both performance and personalization.