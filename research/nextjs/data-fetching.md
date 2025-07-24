# Next.js: Data Fetching Guide

## Server Components Fetching
By default, components in the App Router are Server Components that can fetch data directly.

### Using `fetch` API
```typescript
// app/posts/page.tsx
export default async function PostsPage() {
  // This fetch happens on the server
  const res = await fetch('https://api.vercel.app/blog')
  const posts = await res.json()
  
  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}

// With error handling
export default async function PostsPage() {
  try {
    const res = await fetch('https://api.vercel.app/blog')
    
    if (!res.ok) {
      throw new Error('Failed to fetch posts')
    }
    
    const posts = await res.json()
    
    return (
      <ul>
        {posts.map((post) => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>
    )
  } catch (error) {
    return <div>Error loading posts</div>
  }
}
```

### Using ORM or Database Client
```typescript
// app/users/page.tsx
import { prisma } from '@/lib/prisma'

export default async function UsersPage() {
  // Direct database query in Server Component
  const users = await prisma.user.findMany()
  
  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  )
}
```

## Client Components Fetching
For client-side data fetching, mark components with `'use client'`.

### Using React's `use` Hook
```typescript
'use client'
import { use } from 'react'

// Parent Server Component
export default async function PostsPage() {
  const postsPromise = fetch('https://api.vercel.app/blog').then(res => res.json())
  
  return <Posts posts={postsPromise} />
}

// Child Client Component
function Posts({ posts }: { posts: Promise<Post[]> }) {
  const allPosts = use(posts)
  
  return (
    <ul>
      {allPosts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

### Using Community Libraries (SWR)
```typescript
'use client'
import useSWR from 'swr'

const fetcher = (url: string) => fetch(url).then(res => res.json())

export default function Profile() {
  const { data, error, isLoading } = useSWR('/api/user', fetcher)
  
  if (error) return <div>Failed to load</div>
  if (isLoading) return <div>Loading...</div>
  
  return <div>Hello {data.name}!</div>
}
```

### Using React Query
```typescript
'use client'
import { useQuery } from '@tanstack/react-query'

export default function Posts() {
  const { data, error, isLoading } = useQuery({
    queryKey: ['posts'],
    queryFn: () => fetch('/api/posts').then(res => res.json()),
  })
  
  if (isLoading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>
  
  return (
    <ul>
      {data.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

## Caching Strategies

### Request Memoization
Automatic deduplication of `fetch` requests:
```typescript
// These will only make one request
async function getUser(id: string) {
  const res = await fetch(`/api/users/${id}`)
  return res.json()
}

// In the same render pass
const user1 = await getUser('123') // Makes request
const user2 = await getUser('123') // Returns memoized result
```

### Data Cache
```typescript
// Force cache
const staticData = await fetch('https://api.example.com/data', {
  cache: 'force-cache' // Default behavior
})

// No cache
const dynamicData = await fetch('https://api.example.com/data', {
  cache: 'no-store'
})

// Revalidate after time
const revalidatedData = await fetch('https://api.example.com/data', {
  next: { revalidate: 3600 } // Revalidate every hour
})
```

### Using `cache` Function
For non-fetch data access:
```typescript
import { cache } from 'react'
import { db } from '@/lib/db'

export const getUser = cache(async (id: string) => {
  const user = await db.user.findUnique({ where: { id } })
  return user
})
```

## Streaming Data
Improve perceived performance by streaming data progressively.

### Using `loading.js`
```typescript
// app/posts/loading.tsx
export default function Loading() {
  return <PostsSkeleton />
}

// app/posts/page.tsx
export default async function PostsPage() {
  const posts = await getPosts() // This can take time
  return <PostsList posts={posts} />
}
```

### Using `<Suspense>`
```typescript
import { Suspense } from 'react'

export default function PostsPage() {
  return (
    <div>
      <h1>Posts</h1>
      <Suspense fallback={<PostsSkeleton />}>
        <Posts />
      </Suspense>
    </div>
  )
}

async function Posts() {
  const posts = await getPosts()
  return <PostsList posts={posts} />
}
```

### Streaming with Parallel Data Fetching
```typescript
export default async function Dashboard() {
  // Start all promises in parallel
  const analyticsPromise = getAnalytics()
  const revenuePromise = getRevenue()
  const customersPromise = getCustomers()
  
  return (
    <>
      <Suspense fallback={<AnalyticsSkeleton />}>
        <Analytics promise={analyticsPromise} />
      </Suspense>
      
      <Suspense fallback={<RevenueSkeleton />}>
        <Revenue promise={revenuePromise} />
      </Suspense>
      
      <Suspense fallback={<CustomersSkeleton />}>
        <Customers promise={customersPromise} />
      </Suspense>
    </>
  )
}
```

## Best Practices
1. **Prefer Server Components** for data fetching when possible
2. **Use caching** to improve performance
3. **Implement streaming** for better user experience
4. **Handle errors gracefully** with error boundaries
5. **Optimize with parallel requests** when fetching multiple resources
6. **Use loading states** to provide feedback during data fetching

## Mutation and Server Actions
For data mutations, use Server Actions:

```typescript
// app/actions.ts
'use server'

export async function createPost(formData: FormData) {
  const title = formData.get('title')
  const content = formData.get('content')
  
  await db.post.create({
    data: { title, content }
  })
  
  revalidatePath('/posts')
}

// app/new-post/page.tsx
import { createPost } from './actions'

export default function NewPost() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit">Create Post</button>
    </form>
  )
}
```