function Filter(prop) {
    const schema = prop.schema;

    if (!schema)
        return <></>

    const props = schema["items"]["properties"]
    const columns = Object.keys(props);

    const opts = columns.map((c, idx) => 
        <option value={props[c]["title"]}>{props[c]["title"]}</option>
    )

    const filterData = () => {
        // TODO:
    }

    return (
        <div>
            <label for="columns">&nbsp; Filter by:</label>
            <select name="columns" id="columns">
                { opts }
            </select>
            <button onClick={filterData}> Filter </button>
            <br></br>
        </div>
    );
}

export default Filter;