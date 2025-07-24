# Next.js App Router: Routing Guide

## File-System Based Routing
Routes are created using folders in the `app` directory. Each folder represents a route segment.

### Basic Structure
```
app/
├── page.js          # / route
├── about/
│   └── page.js      # /about route
└── blog/
    ├── page.js      # /blog route
    └── [slug]/
        └── page.js  # /blog/[slug] dynamic route
```

## Creating Pages
`page.js` files make routes publicly accessible:

```typescript
// app/page.tsx
export default function Page() {
  return <h1>Hello, Next.js!</h1>
}

// app/about/page.tsx
export default function AboutPage() {
  return <h1>About</h1>
}
```

## Layouts
Shared UI across multiple pages that preserve state during navigation:

```typescript
// app/layout.tsx - Root layout (required)
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <nav>
          {/* Navigation here */}
        </nav>
        <main>{children}</main>
      </body>
    </html>
  )
}

// app/dashboard/layout.tsx - Nested layout
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <section>
      <aside>
        {/* Dashboard sidebar */}
      </aside>
      <div>{children}</div>
    </section>
  )
}
```

## Nested Routes
Create nested routes by nesting folders:

```
app/
└── blog/
    ├── page.js           # /blog
    └── [slug]/
        ├── page.js       # /blog/[slug]
        └── comments/
            └── page.js   # /blog/[slug]/comments
```

## Dynamic Routes
Use `[segmentName]` to create dynamic route segments:

```typescript
// app/blog/[slug]/page.tsx
export default async function BlogPostPage({
  params,
}: {
  params: { slug: string }
}) {
  const post = await getPost(params.slug)
  
  return (
    <div>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </div>
  )
}

// Multiple dynamic segments
// app/shop/[category]/[product]/page.tsx
export default async function ProductPage({
  params,
}: {
  params: { category: string; product: string }
}) {
  // Access params.category and params.product
}
```

### Catch-all Routes
```typescript
// app/docs/[...slug]/page.tsx
// Matches /docs/a, /docs/a/b, /docs/a/b/c, etc.
export default function DocsPage({
  params,
}: {
  params: { slug: string[] }
}) {
  // params.slug is an array
}

// Optional catch-all
// app/docs/[[...slug]]/page.tsx
// Also matches /docs (without segments)
```

## Linking Between Pages
Use `<Link>` component from `next/link`:

```typescript
import Link from 'next/link'

export default function Navigation() {
  return (
    <nav>
      <Link href="/">Home</Link>
      <Link href="/about">About</Link>
      <Link href="/blog/hello-world">Read Post</Link>
    </nav>
  )
}

// Dynamic links
export default async function PostList() {
  const posts = await getPosts()
  
  return (
    <ul>
      {posts.map((post) => (
        <li key={post.slug}>
          <Link href={`/blog/${post.slug}`}>{post.title}</Link>
        </li>
      ))}
    </ul>
  )
}
```

## Route Groups
Organize routes without affecting URL structure using `(folderName)`:

```
app/
├── (marketing)/
│   ├── about/page.js     # /about
│   └── contact/page.js   # /contact
└── (shop)/
    ├── products/page.js  # /products
    └── cart/page.js      # /cart
```

## Parallel Routes
Render multiple pages in the same layout using `@folder`:

```
app/
├── layout.js
├── @team/
│   └── page.js
└── @analytics/
    └── page.js
```

```typescript
// app/layout.tsx
export default function Layout({
  children,
  team,
  analytics,
}: {
  children: React.ReactNode
  team: React.ReactNode
  analytics: React.ReactNode
}) {
  return (
    <>
      {children}
      {team}
      {analytics}
    </>
  )
}
```

## Route Handlers
Create API endpoints using `route.js`:

```typescript
// app/api/posts/route.ts
import { NextResponse } from 'next/server'

export async function GET() {
  const posts = await getPosts()
  return NextResponse.json(posts)
}

export async function POST(request: Request) {
  const body = await request.json()
  const newPost = await createPost(body)
  return NextResponse.json(newPost)
}
```

## Metadata
Configure page metadata:

```typescript
// Static metadata
export const metadata = {
  title: 'About Us',
  description: 'Learn more about our company',
}

// Dynamic metadata
export async function generateMetadata({ params }) {
  const post = await getPost(params.slug)
  
  return {
    title: post.title,
    description: post.excerpt,
  }
}
```

## Loading and Error States

```typescript
// app/loading.tsx
export default function Loading() {
  return <div>Loading...</div>
}

// app/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error
  reset: () => void
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  )
}
```

## Best Practices
- Use layouts for shared UI elements
- Implement loading states for better UX
- Use route groups for organization
- Leverage parallel routes for complex layouts
- Always include error boundaries