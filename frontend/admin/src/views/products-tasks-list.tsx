import {Button, Table} from "antd";
import {useEffect, useState} from "react";
import ProductsTasksApi, { ProductsTasks } from "../api/products-tasks";

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
        render: (_: string, record: Record<string, any>) => {
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

export default function ProductsTasksList() {
    const [tasks, setTasks] = useState<Array<Record<string, any>>>([]);

    async function fetchTasks(): Promise<Array<ProductsTasks>> {
        const api = new ProductsTasksApi();
        return await api.getProductsTasks();

    }

    useEffect(() => {
        fetchTasks().then(result => {
            setTasks(result.map((item) => productsTasksDisplay(item)))
        });
    }, [])

    return (
        <div>
            <h2>Tasks list</h2>
            <Table pagination={false} dataSource={tasks} columns={columns} rowKey="id"/>
        </div>
    );
}