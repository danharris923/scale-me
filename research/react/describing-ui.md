# React: Describing the UI

## Core Concept
React builds user interfaces from "isolated pieces of UI called *components*" - JavaScript functions that can include markup.

## Key Techniques

### 1. Creating Components
```javascript
function Profile() {
  return (
    <img
      src="https://i.imgur.com/MK3eW3As.jpg"
      alt="Katherine Johnson"
    />
  );
}

export default function Gallery() {
  return (
    <section>
      <h1>Amazing scientists</h1>
      <Profile />
      <Profile />
      <Profile />
    </section>
  );
}
```

### 2. Component Composition
- Components can be nested and reused
- Can create complex UIs from simple building blocks
- Components are regular JavaScript functions that return markup

### 3. Importing/Exporting Components
Split components into separate files for better organization:

```javascript
// Profile.js
export default function Profile() {
  return <img src="..." alt="..." />;
}

// Gallery.js
import Profile from './Profile.js';

export default function Gallery() {
  return (
    <section>
      <Profile />
    </section>
  );
}
```

### 4. JSX Syntax
HTML-like syntax within JavaScript with specific rules:
- All tags must be closed (`<br />`)
- Use `className` instead of `class`
- Wrap multiple elements in a fragment `<>...</>`
- camelCase for most HTML attributes

```javascript
return (
  <>
    <h1>Welcome</h1>
    <img 
      className="avatar"
      src={user.imageUrl}
      alt={`Photo of ${user.name}`}
    />
  </>
);
```

### 5. JavaScript in Components
Use curly braces `{}` to embed JavaScript expressions:

```javascript
const user = {
  name: 'Hedy Lamarr',
  imageUrl: 'https://i.imgur.com/yXOvdOSs.jpg',
  imageSize: 90,
};

function Avatar() {
  return (
    <img
      src={user.imageUrl}
      alt={'Photo of ' + user.name}
      style={{
        width: user.imageSize,
        height: user.imageSize
      }}
    />
  );
}
```

### 6. Props
Pass data between components:

```javascript
function Avatar({ person, size = 100 }) {
  return (
    <img
      src={getImageUrl(person)}
      alt={person.name}
      width={size}
      height={size}
    />
  );
}

function Profile() {
  return (
    <Avatar
      person={{ name: 'Lin Lanying', imageId: '1bX5QH6' }}
      size={100}
    />
  );
}
```

### 7. Conditional Rendering
Use JavaScript operators to render conditionally:

```javascript
// Using ternary operator
function Item({ name, isPacked }) {
  return (
    <li className="item">
      {isPacked ? name + ' ✅' : name}
    </li>
  );
}

// Using && operator
function Item({ name, isPacked }) {
  return (
    <li className="item">
      {name} {isPacked && '✅'}
    </li>
  );
}

// Using if statements
function Item({ name, isPacked }) {
  let itemContent = name;
  if (isPacked) {
    itemContent = name + ' ✅';
  }
  return (
    <li className="item">
      {itemContent}
    </li>
  );
}
```

### 8. Rendering Lists
Use `map()` to transform data into components:

```javascript
const people = [
  { id: 0, name: 'Creola Katherine Johnson' },
  { id: 1, name: 'Mario José Molina-Pasquel Henríquez' },
  { id: 2, name: 'Mohammad Abdus Salam' },
];

function List() {
  const listItems = people.map(person =>
    <li key={person.id}>
      {person.name}
    </li>
  );
  return <ul>{listItems}</ul>;
}
```

Important: Always provide a unique `key` for list items!

### 9. Pure Components
Functions that:
- Don't modify external state
- Return same output for same inputs
- Don't cause side effects during rendering

```javascript
// Pure component
function Recipe({ drinkers }) {
  return (
    <ol>    
      <li>Boil {drinkers} cups of water.</li>
      <li>Add {drinkers} spoons of tea.</li>
      <li>Add {0.5 * drinkers} spoons of spice.</li>
      <li>Add milk to taste.</li>
    </ol>
  );
}

// Impure - modifies external variable
let guest = 0;
function Cup() {
  guest = guest + 1;  // Bad! Modifying external state
  return <h2>Tea cup for guest #{guest}</h2>;
}
```

## UI as a Tree
React conceptualizes UI as two types of trees:
- **Render tree**: Component relationships and hierarchy
- **Module dependency tree**: Import relationships between files

Understanding these trees helps with:
- Performance optimization
- State management
- Bundle size optimization