import {Button, Table, Input, Row, Col, Divider, Space} from "antd";
import { useEffect, useState} from "react";
import { Link } from "react-router-dom";
import productsTasksApi, { ProductsTasks } from "../../api/products-tasks";
import {isValidHttpUrl} from "../../utils/validators";

const { Search } = Input;

const getColumns = (deleteCallback: Function) => [
    {
        title: "Object Id",
        dataIndex: "id",
        key: 'id',
    },
    {
        title: "Created",
        dataIndex: "created",
        key: 'created',
    },
    {
        title: "Status",
        dataIndex: "status",
        key: 'status',
    },
    {
        title: "Url",
        dataIndex: "pageUrl",
        key: 'pageUrl',
        render: (_: string, record: Record<string, any>) => {
            return (
                <a href={record.pageUrl}>{record.pageUrl}</a>
            )
        },
    },
    {
        title: "Count",
        dataIndex: "count",
        key: 'count',
    },
    {
        title: "Action",
        key: 'action',
        render: (_: string, record: Record<string, any>) => (
            <Space>
                <Button disabled={record.count === 0} type="primary">
                    <Link to={`/tasks/${record.id}`}>Show results</Link>
                </Button>
                <Button onClick={() => { deleteCallback(record.id)} } danger type="primary">
                    Delete
                </Button>

            </Space>

        ),
    },
];

const productsTasksDisplay = (productsTasks: ProductsTasks): Record<string, any> => {
    const created = new Date(productsTasks.timestamp * 1000);
    return {
        id: productsTasks.id,
        created: `${created.toLocaleDateString()} | ${created.toLocaleTimeString()}`,
        status: productsTasks.status,
        pageUrl: productsTasks.pageUrl,
        count: productsTasks.count
    }
}

const fetchTasksRequest = async (): Promise<Array<ProductsTasks>> => {
    return await productsTasksApi.getProductsTasks();
}
const addTaskRequest = async(url: string): Promise<ProductsTasks> => {
    return await productsTasksApi.addTask(url);
}
const deleteTaskRequest = async(objectId: string): Promise<boolean> => {
    return await productsTasksApi.deleteTask(objectId);
}


export default function ProductsTasksList() {
    const [tasks, setTasks] = useState<Array<Record<string, any>>>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        fetchTasksRequest().then(result => {
            setTasks(result.map((item) => productsTasksDisplay(item)));
            setIsLoading(false);
        });
    }, [])
    const createTask = (value: string) => {
        if (isLoading) { return; }
        if (!isValidHttpUrl(value)) {
            alert("Invalid URL");
            return;
        }
        setIsLoading(true);
        addTaskRequest(value).then(result => {
            setTasks([...tasks, result])
            setIsLoading(false);
        });
    }
    const deleteTask = (objectId: string) => {
        if (isLoading) { return; }
        setIsLoading(true);
        deleteTaskRequest(objectId).then((deleted) => {
            if (!deleted){
                alert(`Could not delete the task ${objectId}`)
                return;
            }
            setTasks([...tasks.filter(task => task.id !== objectId)])
            setIsLoading(false);
        });
    }

    return (
        <div>
            <h2>Tasks list</h2>
            <Row justify="center">
                <Col xs={24} sm={12}>
                    <Input.Group compact>
                        <Search onSearch={ createTask } placeholder="Enter page URL"
                                enterButton="Add Task" size="large" loading={isLoading} />
                    </Input.Group>
                </Col>
            </Row>
            <Divider dashed />
            <Row>
                <Col span={24}>
                    <Table loading={isLoading} scroll={{ x: 900 }} pagination={false}
                           dataSource={tasks} columns={getColumns(deleteTask)} rowKey="id"/>
                </Col>
            </Row>

        </div>
    );
}