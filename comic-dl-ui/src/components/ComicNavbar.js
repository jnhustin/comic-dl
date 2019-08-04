import React        from 'react'
import Navbar       from 'react-bootstrap/Navbar'
import Nav          from 'react-bootstrap/Nav'
import Button       from 'react-bootstrap/Button'
import InputGroup   from 'react-bootstrap/InputGroup'
import FormControl  from 'react-bootstrap/FormControl'

const ComicNavbar = ({
  handleDownload,
  handleRemove,
  isShowAddCoverInput,
  handleAddCoverImage,
  handleAddCoverInputChange,
  handleSearch,
  handleChange,
}) => {

  return (
    <React.Fragment>
      <Navbar sticky="top">
        <Nav>
          <Button className='btn-danger mr-2' onClick={handleRemove}>Remove Panels</Button>
          <Button className='btn-success'     onClick={handleDownload}>Download</Button>
          <div>
            <InputGroup className="ml-2">
              <FormControl placeholder="add chapter" onChange={handleChange} />
              <InputGroup.Append>
                <Button
                  onClick={handleSearch}
                  variant="dark">
                  Add
                </Button>
              </InputGroup.Append>
            </InputGroup>
          </div>
        </Nav>
      </Navbar>

      <Navbar>
        {
          isShowAddCoverInput && (
            <InputGroup className="mb-3">
              <FormControl placeholder="paste cover URL here" onChange={handleAddCoverInputChange} />
              <InputGroup.Append>
                <Button
                  onClick={handleAddCoverImage}
                  variant="outline-secondary">
                  Add
                </Button>
              </InputGroup.Append>
            </InputGroup>
          )
        }
      </Navbar>
    </React.Fragment>
  )
}

export default ComicNavbar;
