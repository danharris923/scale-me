# React: Adding Interactivity

## Key Concepts

### 1. Event Handling
React allows adding event handlers to JSX. Event handlers are functions triggered by user interactions.

```javascript
function Button() {
  function handleClick() {
    alert('You clicked me!');
  }

  return (
    <button onClick={handleClick}>
      Click me
    </button>
  );
}
```

Event handler conventions:
- Usually defined inside components
- Names start with `handle` followed by event name
- Passed as props (not called): `onClick={handleClick}` not `onClick={handleClick()}`

### 2. State Management
State represents "component-specific memory" - data that can change over time.

### 3. The `useState` Hook
```javascript
import { useState } from 'react';

function Gallery() {
  const [index, setIndex] = useState(0);
  const [showMore, setShowMore] = useState(false);

  function handleNextClick() {
    setIndex(index + 1);
  }

  function handleMoreClick() {
    setShowMore(!showMore);
  }

  return (
    <>
      <button onClick={handleNextClick}>
        Next
      </button>
      <button onClick={handleMoreClick}>
        {showMore ? 'Hide' : 'Show'} details
      </button>
      {showMore && <p>Details here...</p>}
    </>
  );
}
```

### 4. State Rules and Best Practices

#### Never Modify State Directly
```javascript
// ❌ Wrong - mutating state
const [position, setPosition] = useState({ x: 0, y: 0 });
position.x = 5; // Don't do this!

// ✅ Correct - creating new object
setPosition({ x: 5, y: 0 });
```

#### State Updates Trigger Re-renders
- Setting state requests a new render
- React will re-render component with new state values
- State behaves like a "snapshot" for each render

#### Multiple State Updates
```javascript
// State updates are batched
function handleClick() {
  setNumber(number + 1); // setNumber(0 + 1)
  setNumber(number + 1); // setNumber(0 + 1)
  setNumber(number + 1); // setNumber(0 + 1)
  // Still only increments by 1!
}

// Use updater function for multiple updates
function handleClick() {
  setNumber(n => n + 1); // setNumber(0 => 1)
  setNumber(n => n + 1); // setNumber(1 => 2)
  setNumber(n => n + 1); // setNumber(2 => 3)
  // Increments by 3!
}
```

### 5. Updating Objects in State
Use spread syntax to create copies:

```javascript
const [person, setPerson] = useState({
  name: 'Niki de Saint Phalle',
  artwork: {
    title: 'Blue Nana',
    city: 'Hamburg',
    image: 'https://i.imgur.com/Sd1AgUOm.jpg',
  }
});

// Update nested object
function handleCityChange(e) {
  setPerson({
    ...person,
    artwork: {
      ...person.artwork,
      city: e.target.value
    }
  });
}
```

### 6. Updating Arrays in State
Create new arrays instead of mutating:

```javascript
const [artists, setArtists] = useState([]);

// ✅ Adding
setArtists([...artists, { id: nextId, name: name }]);

// ✅ Removing
setArtists(artists.filter(a => a.id !== artist.id));

// ✅ Transforming
setArtists(artists.map(artist => {
  if (artist.id === targetId) {
    return { ...artist, name: newName };
  } else {
    return artist;
  }
}));

// ✅ Replacing
setArtists([
  ...artists.slice(0, insertAt),
  { id: nextId, name: name },
  ...artists.slice(insertAt)
]);

// ✅ Sorting (make copy first)
setArtists([...artists].sort((a, b) => a.name.localeCompare(b.name)));
```

### 7. Using Immer for Complex Updates
For complex nested updates, consider using Immer:

```javascript
import { useImmer } from 'use-immer';

const [person, updatePerson] = useImmer({
  name: 'Niki de Saint Phalle',
  artwork: {
    title: 'Blue Nana',
    city: 'Hamburg',
  }
});

function handleCityChange(e) {
  updatePerson(draft => {
    draft.artwork.city = e.target.value;
  });
}
```

## Key Principles
- Treat state as immutable (read-only)
- Always create new objects/arrays when updating
- Use functional updates for reliable state changes
- State updates are asynchronous and batched
- Each render has its own "snapshot" of state