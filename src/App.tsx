import { useEffect, useRef, useState } from 'react'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Button from 'react-bootstrap/Button'
import Spinner from 'react-bootstrap/Spinner'
import 'bootstrap/dist/css/bootstrap.min.css'

import Todo from './components/Todo/Todo'

import all_todos from './data/all_todos.json'
import summer_todos from './data/summer_todos.json'
import autumn_todos from './data/autumn_todos.json'
import winter_todos from './data/winter_todos.json'
import spring_todos from './data/spring_todos.json'
import jan_todos from './data/month_0_todos.json'
import feb_todos from './data/month_1_todos.json'
import mar_todos from './data/month_2_todos.json'
import apr_todos from './data/month_3_todos.json'
import may_todos from './data/month_4_todos.json'
import jun_todos from './data/month_5_todos.json'
import jul_todos from './data/month_6_todos.json'
import aug_todos from './data/month_7_todos.json'
import sep_todos from './data/month_8_todos.json'
import oct_todos from './data/month_9_todos.json'
import nov_todos from './data/month_10_todos.json'
import dec_todos from './data/month_11_todos.json'

import { Todo as TodoType } from './model'

import './App.css'

const App = () => {

    const allTodos = useRef<TodoType[] | null>(null)

    // const [filters, setFilters] = useState<string[]>([])
    const [todo, setTodo] = useState<TodoType | null>(null)

    const loadTodos = (x: TodoType[]) => {
        const today = new Date()
        return x.filter(y => y.daysOfWeek.length === 0 || y.daysOfWeek.indexOf(today.getDay()) !== -1)
    }

    const handleNewItemClick = () => {
        if (!allTodos.current) return
        setTodo(allTodos.current[Math.floor(Math.random() * allTodos.current.length)])
    }

    useEffect(() => {
        const _allTodos = all_todos.items
        allTodos.current = _allTodos
        const today = new Date()
        if ([2, 3, 4].indexOf(today.getMonth()) !== -1)
            allTodos.current = [...allTodos.current, ...loadTodos(spring_todos.items)]
        if ([5, 6, 7].indexOf(today.getMonth()) !== -1)
            allTodos.current = [...allTodos.current, ...loadTodos(summer_todos.items)]
        if ([8, 9, 10].indexOf(today.getMonth()) !== -1)
            allTodos.current = [...allTodos.current, ...loadTodos(autumn_todos.items)]
        if ([11, 0, 1].indexOf(today.getMonth()) !== -1)
            allTodos.current = [...allTodos.current, ...loadTodos(winter_todos.items)]
        if (today.getMonth() === 0)
            allTodos.current = [...allTodos.current, ...loadTodos(jan_todos.items)]
        if (today.getMonth() === 1)
            allTodos.current = [...allTodos.current, ...loadTodos(feb_todos.items)]
        if (today.getMonth() === 2)
            allTodos.current = [...allTodos.current, ...loadTodos(mar_todos.items)]
        if (today.getMonth() === 3)
            allTodos.current = [...allTodos.current, ...loadTodos(apr_todos.items)]
        if (today.getMonth() === 4)
            allTodos.current = [...allTodos.current, ...loadTodos(may_todos.items)]
        if (today.getMonth() === 5)
            allTodos.current = [...allTodos.current, ...loadTodos(jun_todos.items)]
        if (today.getMonth() === 6)
            allTodos.current = [...allTodos.current, ...loadTodos(jul_todos.items)]
        if (today.getMonth() === 7)
            allTodos.current = [...allTodos.current, ...loadTodos(aug_todos.items)]
        if (today.getMonth() === 8)
            allTodos.current = [...allTodos.current, ...loadTodos(sep_todos.items)]
        if (today.getMonth() === 9)
            allTodos.current = [...allTodos.current, ...loadTodos(oct_todos.items)]
        if (today.getMonth() === 10)
            allTodos.current = [...allTodos.current, ...loadTodos(nov_todos.items)]
        if (today.getMonth() === 11)
            allTodos.current = [...allTodos.current, ...loadTodos(dec_todos.items)]
        setTodo(allTodos.current[Math.floor(Math.random() * allTodos.current.length)])
    }, [])

    return (
        <Container fluid>
            <Row>
                <Col xs={0} md={3} />
                <Col xs={12} md={6}>
                    <Row className='pt-3'>
                        <Col><h1 className='display-4 mt-4 text-center'>What should I do in Evansville?</h1></Col>
                    </Row>
                    <Row>
                        <Col>
                            {
                                todo ?
                                <Todo item={todo} /> :
                                <div className='text-center'><Spinner /></div>
                            }
                        </Col>
                    </Row>
                    <Row className='mt-3'>
                        <Col className='text-center'>
                            <Button variant='secondary' onClick={handleNewItemClick}>Something else!</Button>
                        </Col>
                    </Row>
                </Col>
                <Col xs={0} md={3} />
            </Row>
            <div className='footer'>
                <Button variant='link' className='text-decoration-none' href='mailto:graham@matthewsapps.com'>Contact Me</Button>
            </div>
        </Container>
    )
}

export default App