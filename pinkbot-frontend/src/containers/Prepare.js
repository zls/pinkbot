import React, { Component } from "react";
import { FormGroup, Button, Form, FormControl, Table, Row, Grid, Col, Well } from "react-bootstrap";
import "./Prepare.css";

var alchemy_spells = [
    {
        Name: "Analyze Truth",
        Drain: "F-2",
        Link: "foo",
    },
    {
        Name: "Armor",
        Drain: "F-2",
        Link: "foo",
        Bonus: 2
    }

];

console.log(alchemy_spells[0].Name);

class PrepareFormSpell extends React.Component {
    render() {
        const listItems = alchemy_spells.map((n) => 
            <option value={n.Name}>{n.Name}</option>
        );
        return (
            <FormGroup controlId="prepareType">
                <FormControl componentClass="select" placeholder="select">
                    {listItems}
                </FormControl>
            </FormGroup>
        )
    }
}

class PrepareFormForce extends React.Component {
    render() {
        return (
            <FormGroup controlId="prepareForce">
                <FormControl type="text" placeholder="force" />
            </FormGroup>
        )
    }
}

class PrepareFormLynchpin extends React.Component {
    render() {
        return (
            <FormGroup controlId="prepareLynchpin">
                <FormControl type="text" placeholder="lynchpin" />
            </FormGroup>
        )
    }
}

class PrepareFormTrigger extends React.Component {
    render() {
        return (
            <FormGroup controlId="prepareTrigger">
                <FormControl componentClass="select" placeholder="select">
                    <option value="command">Command</option>
                    <option value="contact">Contact</option>
                    <option value="time">Time</option>
                </FormControl>
            </FormGroup>
        )
    }
}


class PrepareForm extends React.Component {
    constructor(props, context) {
        super(props, context);

        this.handleChange = this.handleChange.bind(this);
        this.state = {
            value: ''
        };
    }

    getValidationState() {
        const length = this.state.value.length;
        if (length > 10) return 'success';
        else if (length > 5) return 'warning';
        else if (length > 0) return 'error';
        return null;
    }
    
    handleChange(e) {
        this.setState({ value: e.target.value });
    }

    render() {
        return (
            <div>
            <Form inline>
                <PrepareFormSpell />{' '}
                <PrepareFormForce />{' '}
                <PrepareFormLynchpin />{' '}
                <PrepareFormTrigger/>{' '}
                <Button type="submit">Prepare</Button>
            </Form>
            </div>
        )

    }
}

var prepared_spells = [
    {
        Name: "Flamethrower",
        Trigger: "touch",
        Lynchpin: "Marble wrapped in coloured tissue papper",
        Force: 4,
        Potency: 4,
    }
]

class Prepared extends React.Component {
    render() {
        const spells = prepared_spells.map((n) => 
            <tr>
                <td>{n.Name}</td>
                <td>{n.Trigger}</td>
                <td>{n.Lynchpin}</td>
                <td>{n.Force}</td>
                <td>{n.Potency}</td>
            </tr>
        );
        return (
            <div>
            <Table striped bordered condensed hover>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Trigger</th>
                        <th>Lynchpin</th>
                        <th>Force</th>
                        <th>Potency</th>
                    </tr>
                </thead>
                <tbody>
                    {spells}
                </tbody>
            </Table>
            </div>
        )

    }
}

export default class Prepare extends Component {
  render() {
    return (
      <div className="Prepare">
        <div className="lander">
            <Grid>
                <Row className="row">
                    <Col>
                        <PrepareForm />
                    </Col>
                </Row>
                <Row className="row">
                    <Col>
                        <Well>
                            <Prepared />
                        </Well>
                    </Col>
                </Row>
            </Grid>
        </div>
      </div>
    );
  }
}