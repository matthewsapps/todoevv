import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Button from 'react-bootstrap/Button'

import { TextBlock, Todo as TodoType } from "../../model"

interface TodoProps {
    item: TodoType
}

const Todo = ({ item }: TodoProps) => {

    const renderDescriptionBlock = (x: TextBlock) => {
        if (x.element === 'p')
            return <p key={x.text} className='text-center'>{x.text}</p>
        if (x.element === 'button')
            return <div key={x.text} className='text-center'><Button variant='dark' href={x.href} target='_blank'>{x.text}</Button></div>
        return <>{x.text}</>
    }

    return (
        <Container className='mt-5'>
            <Row>
                <Col>
                    <h2 className='display-3 fs-3 text-center'>{item.title}</h2>
                    { item.description.map(renderDescriptionBlock) }
                </Col>
            </Row>
        </Container>
    )
}

export default Todo