import {Button, Table} from "antd";
import {useEffect, useState} from "react";
import ProductsTasksApi, { ProductsTasksDto } from "../api/products-tasks";

const columns = [
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
        render: (_: string, record: ProductsTasksDto) => {
            return (
                <a href={record.pageUrl}>{record.pageUrl}</a>
            )
        }
    },
    {
        title: "Count",
        dataIndex: "count",
        key: 'count',
    },
    {
        title: "Action",
        key: 'action',
        render: () => (
            <Button type="primary">Show results</Button>
        )
    },
];

export default function TasksList() {
    const [tasks, setTasks] = useState<Array<ProductsTasksDto>>([]);

    async function fetchTasks(): Promise<Array<ProductsTasksDto>> {
        const api = new ProductsTasksApi();
        return await api.getProductsTasks();

    }
    useEffect(() => {
        fetchTasks().then(result => {
            setTasks(result)
        });
    }, [])

    return (
        <div>
            <h2>Tasks list</h2>
            <Table pagination={false} dataSource={tasks} columns={columns} rowKey="id"/>
        </div>
    );
}