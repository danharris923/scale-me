# React: Managing State

## State Management Principles

### 1. State Structure Best Practices
- **Avoid redundant or duplicate state**
- State should describe the UI's different visual conditions
- Calculate values during rendering when possible

Example of avoiding redundant state:
```javascript
// ❌ Bad - redundant state
const [firstName, setFirstName] = useState('');
const [lastName, setLastName] = useState('');
const [fullName, setFullName] = useState('');

// ✅ Good - calculate during render
const [firstName, setFirstName] = useState('');
const [lastName, setLastName] = useState('');
const fullName = firstName + ' ' + lastName;
```

### 2. Sharing State Between Components
"Lift state up" to the closest common parent component:

```javascript
// Parent component holds shared state
function Parent() {
  const [activeIndex, setActiveIndex] = useState(0);
  
  return (
    <>
      <Panel 
        title="About"
        isActive={activeIndex === 0}
        onShow={() => setActiveIndex(0)}
      />
      <Panel
        title="Etymology" 
        isActive={activeIndex === 1}
        onShow={() => setActiveIndex(1)}
      />
    </>
  );
}

// Child components receive state via props
function Panel({ title, isActive, onShow }) {
  return (
    <section>
      <h3>{title}</h3>
      {isActive ? (
        <p>Content...</p>
      ) : (
        <button onClick={onShow}>Show</button>
      )}
    </section>
  );
}
```

### 3. State Preservation and Reset
React preserves component state based on position in the tree:

```javascript
// State is preserved when component stays in same position
function Counter() {
  const [score, setScore] = useState(0);
  return <div>{score}</div>;
}

// Use key to force state reset
<Counter key={person.id} person={person} />
```

### 4. Advanced State Management: Reducers
Consolidate state update logic in a single function:

```javascript
import { useReducer } from 'react';

function tasksReducer(tasks, action) {
  switch (action.type) {
    case 'added': {
      return [...tasks, {
        id: action.id,
        text: action.text,
        done: false
      }];
    }
    case 'changed': {
      return tasks.map(t => {
        if (t.id === action.task.id) {
          return action.task;
        } else {
          return t;
        }
      });
    }
    case 'deleted': {
      return tasks.filter(t => t.id !== action.id);
    }
    default: {
      throw Error('Unknown action: ' + action.type);
    }
  }
}

function TaskApp() {
  const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);
  
  function handleAddTask(text) {
    dispatch({
      type: 'added',
      id: nextId++,
      text: text,
    });
  }
  
  // ... rest of component
}
```

### 5. Context for Deep Prop Passing
Pass data deeply without explicit prop drilling:

```javascript
import { createContext, useContext } from 'react';

// Create context
const ThemeContext = createContext(null);

// Provide context
function App() {
  const [theme, setTheme] = useState('light');
  
  return (
    <ThemeContext.Provider value={theme}>
      <Page />
    </ThemeContext.Provider>
  );
}

// Consume context
function Button() {
  const theme = useContext(ThemeContext);
  return (
    <button className={theme}>
      Click me
    </button>
  );
}
```

### 6. Scaling with Reducer and Context
Combine reducers and context for complex state management:

```javascript
// Create contexts
const TasksContext = createContext(null);
const TasksDispatchContext = createContext(null);

// Provider component
export function TasksProvider({ children }) {
  const [tasks, dispatch] = useReducer(tasksReducer, initialTasks);
  
  return (
    <TasksContext.Provider value={tasks}>
      <TasksDispatchContext.Provider value={dispatch}>
        {children}
      </TasksDispatchContext.Provider>
    </TasksContext.Provider>
  );
}

// Custom hooks for using context
export function useTasks() {
  return useContext(TasksContext);
}

export function useTasksDispatch() {
  return useContext(TasksDispatchContext);
}

// Usage in components
function TaskList() {
  const tasks = useTasks();
  const dispatch = useTasksDispatch();
  
  return (
    <ul>
      {tasks.map(task => (
        <li key={task.id}>
          {task.text}
          <button onClick={() => {
            dispatch({
              type: 'deleted',
              id: task.id
            });
          }}>
            Delete
          </button>
        </li>
      ))}
    </ul>
  );
}
```

## Key Principles
- Structure state to avoid redundancy
- Lift state up when multiple components need it
- Use keys to control state preservation
- Use reducers for complex state logic
- Use context to avoid prop drilling
- Combine reducers and context for scalable state management