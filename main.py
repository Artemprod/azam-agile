import asyncio
from datetime import datetime
from engene import DatabaseSessionManager
from models.base import ModelBase
from models import init
from repo.access import AccessSettingRepository, AccessLevelSettingRepository, AccessLevelRepository
from repo.assigned import ProjectAssignedRepository, TaskAssignedRepository
from repo.chat import ChatRepository
from repo.message import MessageRepository
from repo.notification import NotificationRepository
from repo.priorety import PriorityRepository
from repo.project import ProjectRepository
from repo.report import ReportRepository
from repo.status import StatusRepository
from repo.task import TaskRepository
from repo.user import UserRepository


async def create_tables():
    session = DatabaseSessionManager(database_url='postgresql+asyncpg://postgres:1234@localhost:5432/agile')
    async with session.engine.begin() as connection:
        await connection.run_sync(init.ModelBase.metadata.create_all)
    print("Database tables created!")


async def insert_initial_data():
    """Создание начальных данных, необходимых для тестов"""
    session = DatabaseSessionManager(database_url='postgresql+asyncpg://postgres:1234@localhost:5432/agile')

    # Создать начальный уровень доступа
    access_level_repo = AccessLevelRepository(async_session_factory=session.async_session_factory)
    role_manager = await access_level_repo.create_access_level(values={"name": "Manager"})
    role_user = await access_level_repo.create_access_level(values={"name": "User"})

    status_repo = StatusRepository(async_session_factory=session.async_session_factory)
    status_task_open = await status_repo.create_status(values={"name": "Open", "type": "task"})
    status_task_in_progress = await status_repo.create_status(values={"name": "In Progress", "type": "task"})

    priority_repo = PriorityRepository(async_session_factory=session.async_session_factory)
    priority_high = await priority_repo.create_priority(values={"name": "High"})
    priority_low = await priority_repo.create_priority(values={"name": "Low"})

    user_repo = UserRepository(async_session_factory=session.async_session_factory)
    new_user = await user_repo.create_user(values={
        "name": "John Manager",
        "email": "manager@example.com",
        "role_id": role_manager.id,
        "avatar": None,
        "created_at": datetime.utcnow()
    })

    print("Initial test data inserted.")
    return {
        "roles": {
            "manager": role_manager,
            "user": role_user,
        },
        "statuses": {
            "task_open": status_task_open,
            "task_in_progress": status_task_in_progress,
        },
        "priorities": {
            "high": priority_high,
            "low": priority_low,
        },
        "new_user": new_user
    }


# Тесты
async def test_access():
    session = DatabaseSessionManager(database_url='postgresql+asyncpg://postgres:1234@localhost:5432/agile')
    access_level_repo = AccessLevelRepository(async_session_factory=session.async_session_factory)
    access_setting_repo = AccessSettingRepository(async_session_factory=session.async_session_factory)
    access_level_setting_repo = AccessLevelSettingRepository(async_session_factory=session.async_session_factory)

    # Создание нового AccessLevel
    new_access_level = await access_level_repo.create_access_level(values={"name": "manager"})
    print(f"Created AccessLevel: {new_access_level}")

    # Создание нового AccessSetting
    new_access_setting = await access_setting_repo.create_access_setting(values={"permission": 'create_project'})
    print(f"Created AccessSetting: {new_access_setting}")

    # Создание новой записи AccessLevelSetting
    new_access_level_setting = await access_level_setting_repo.create_access_level_setting(values={
        "access_level_id": new_access_level.id,
        "access_setting_id": new_access_setting.id,
        "allowed": True
    })
    print(f"Created AccessLevelSetting: {new_access_level_setting}")


async def test_user_repo(initial_data):
    session = DatabaseSessionManager(database_url='postgresql+asyncpg://postgres:1234@localhost:5432/agile')
    user_repo = UserRepository(async_session_factory=session.async_session_factory)

    # Создание нового пользователя с ролью менеджера
    new_user = await user_repo.create_user(values={
        "name": "John Doe",
        "email": "john@example.com",
        "role_id": initial_data["roles"]["manager"].id,
        "avatar": None,
        "created_at": datetime.utcnow()
    })
    print(f"Created User: {new_user}")

    # Получение данных о пользователе
    user_simple = await user_repo.get_user_by_id(new_user.user_id)
    print(f"User without relations: {user_simple}")

    user_with_relations = await user_repo.get_user_with_relations(new_user.user_id)
    print(f"User with relations: {user_with_relations}")


async def test_status_repo():
    session = DatabaseSessionManager(database_url='postgresql+asyncpg://postgres:1234@localhost:5432/agile')
    status_repo = StatusRepository(async_session_factory=session.async_session_factory)

    # Создание нового статуса
    new_status = await status_repo.create_status(values={"name": "Open", "type": "task"})
    print(f"Created Status: {new_status}")

    status_simple = await status_repo.get_status_by_id(new_status.id)
    print(f"Status without relations: {status_simple}")

    status_with_relations = await status_repo.get_status_with_relations(new_status.id)
    print(f"Status with relations: {status_with_relations}")


async def test_priority_repo():
    session = DatabaseSessionManager(database_url='postgresql+asyncpg://postgres:1234@localhost:5432/agile')
    priority_repo = PriorityRepository(async_session_factory=session.async_session_factory)

    # Создание нового приоритета
    new_priority = await priority_repo.create_priority(values={"name": "High"})
    print(f"Created Priority: {new_priority}")

    priority_simple = await priority_repo.get_priority_by_id(new_priority.id)
    print(f"Priority without relations: {priority_simple}")

    priority_with_relations = await priority_repo.get_priority_with_relations(new_priority.id)
    print(f"Priority with relations: {priority_with_relations}")


async def test_notification_repo(initial_data):
    session = DatabaseSessionManager(database_url='postgresql+asyncpg://postgres:1234@localhost:5432/agile')
    notification_repo = NotificationRepository(async_session_factory=session.async_session_factory)

    # Создание нового уведомления
    new_notification = await notification_repo.create_notification(values={
        "content": "This is a notification",
        "user_id": initial_data["new_user"].user_id,
        "sent_at": datetime.utcnow()
    })
    print(f"Created Notification: {new_notification}")

    # Получение данных об уведомлении
    notification_simple = await notification_repo.get_notification_by_id(new_notification.id)
    print(f"Notification without relations: {notification_simple}")

    notification_with_relations = await notification_repo.get_notification_with_relations(new_notification.id)
    print(f"Notification with relations: {notification_with_relations}")


async def test_chat_repo(initial_data):
    session = DatabaseSessionManager(database_url='postgresql+asyncpg://postgres:1234@localhost:5432/agile')
    chat_repo = ChatRepository(async_session_factory=session.async_session_factory)
    project_repo = ProjectRepository(async_session_factory=session.async_session_factory)

    # Создание нового проекта
    project = await project_repo.create_project(values={
        "title": "Project Alpha",
        "description": "Description of Project Alpha",
        "start_date": datetime.utcnow(),
        "deadline": datetime(2023, 12, 31),
        "status_id": initial_data["statuses"]["task_open"].id,
        "owner_id": initial_data["new_user"].user_id,
        "priority_id": initial_data["priorities"]["high"].id
    })

    # Создание нового чата
    new_chat = await chat_repo.create_chat(values={
        "project_id": project.project_id,
        "task_id": None
    })
    print(f"Created Chat: {new_chat}")

    # Получение данных о чате
    chat_simple = await chat_repo.get_chat_by_id(new_chat.chat_id)
    print(f"Chat without relations: {chat_simple}")

    chat_with_relations = await chat_repo.get_chat_with_relations(new_chat.chat_id)
    print(f"Chat with relations: {chat_with_relations}")


async def test_message_repo(initial_data):
    session = DatabaseSessionManager(database_url='postgresql+asyncpg://postgres:1234@localhost:5432/agile')
    message_repo = MessageRepository(async_session_factory=session.async_session_factory)
    chat_repo = ChatRepository(async_session_factory=session.async_session_factory)

    # Создание нового чата
    chat = await chat_repo.create_chat(values={
        "project_id": None,
        "task_id": None
    })

    # Создание нового сообщения
    new_message = await message_repo.create_message(values={
        "content": "This is a message",
        "user_id": initial_data["new_user"].user_id,
        "chat_id": chat.chat_id,
        "sent_at": datetime.utcnow()
    })
    print(f"Created Message: {new_message}")

    # Получение данных о сообщении
    message_simple = await message_repo.get_message_by_id(new_message.message_id)
    print(f"Message without relations: {message_simple}")

    message_with_relations = await message_repo.get_message_with_relations(new_message.message_id)
    print(f"Message with relations: {message_with_relations}")


async def test_project_repo(initial_data):
    session = DatabaseSessionManager(database_url='postgresql+asyncpg://postgres:1234@localhost:5432/agile')
    project_repo = ProjectRepository(async_session_factory=session.async_session_factory)

    # Создание нового проекта
    new_project = await project_repo.create_project(values={
        "title": "Project Beta",
        "description": "Description of Project Beta",
        "start_date": datetime.utcnow(),
        "deadline": datetime(2023, 12, 31),
        "status_id": initial_data["statuses"]["task_in_progress"].id,
        "owner_id": initial_data["new_user"].user_id,
        "priority_id": initial_data["priorities"]["low"].id
    })
    print(f"Created Project: {new_project}")

    project_simple = await project_repo.get_project_by_id(new_project.project_id)
    print(f"Project without relations: {project_simple}")

    project_with_relations = await project_repo.get_project_with_relations(new_project.project_id)
    print(f"Project with relations: {project_with_relations}")


async def test_task_repo(initial_data):
    session = DatabaseSessionManager(database_url='postgresql+asyncpg://postgres:1234@localhost:5432/agile')
    task_repo = TaskRepository(async_session_factory=session.async_session_factory)

    # Создание нового проекта для задачи
    project_repo = ProjectRepository(async_session_factory=session.async_session_factory)
    project = await project_repo.create_project(values={
        "title": "Project Alpha",
        "description": "Description of Project Alpha",
        "owner_id": initial_data["new_user"].user_id,
        "start_date": datetime.utcnow(),
        "deadline": datetime(2023, 12, 31),
        "status_id": initial_data["statuses"]["task_open"].id,
        "priority_id": initial_data["priorities"]["high"].id
    })

    # Создание новой задачи
    new_task = await task_repo.create_task(values={
        "title": "Task 1",
        "description": "Task description",
        "priority_id": initial_data["priorities"]["high"].id,
        "status_id": initial_data["statuses"]["task_open"].id,
        "executor_id": initial_data["new_user"].user_id,
        "project_id": project.project_id,
        "deadline": datetime(2023, 12, 31)
    })
    print(f"Created Task: {new_task}")

    task_simple = await task_repo.get_task_by_id(new_task.task_id)
    print(f"Task without relations: {task_simple}")

    task_with_relations = await task_repo.get_task_with_relations(new_task.task_id)
    print(f"Task with relations: {task_with_relations}")


async def test_project_assigned_repo(initial_data):
    session = DatabaseSessionManager(database_url='postgresql+asyncpg://postgres:1234@localhost:5432/agile')
    project_assigned_repo = ProjectAssignedRepository(async_session_factory=session.async_session_factory)

    # Создание новой записи ProjectAssigned
    new_project_assigned = await project_assigned_repo.create_project_assigned(values={
        "user_id": initial_data["new_user"].user_id,
        "project_id": 1,  # Убедитесь, что ID проекта существует
        "created_at": datetime.utcnow()
    })
    print(f"Created ProjectAssigned: {new_project_assigned}")

    project_assigned_simple = await project_assigned_repo.get_project_assigned_by_id(new_project_assigned.user_id,
                                                                                     new_project_assigned.project_id)
    print(f"ProjectAssigned without relations: {project_assigned_simple}")


async def test_task_assigned_repo(initial_data):
    session = DatabaseSessionManager(database_url='postgresql+asyncpg://postgres:1234@localhost:5432/agile')
    task_assigned_repo = TaskAssignedRepository(async_session_factory=session.async_session_factory)

    # Создание новой записи TaskAssigned
    new_task_assigned = await task_assigned_repo.create_task_assigned(values={
        "user_id": initial_data["new_user"].user_id,
        "task_id": 1,  # Убедитесь, что ID задачи существует
        "created_at": datetime.utcnow()
    })
    print(f"Created TaskAssigned: {new_task_assigned}")

    task_assigned_simple = await task_assigned_repo.get_task_assigned_by_id(new_task_assigned.user_id,
                                                                            new_task_assigned.task_id)
    print(f"TaskAssigned without relations: {task_assigned_simple}")


async def test_report_repo(initial_data):
    session = DatabaseSessionManager(database_url='postgresql+asyncpg://postgres:1234@localhost:5432/agile')
    report_repo = ReportRepository(async_session_factory=session.async_session_factory)
    project_repo = ProjectRepository(async_session_factory=session.async_session_factory)

    # Создание нового проекта (если у вас нет уже созданного проекта, мы можем создать его здесь)
    project = await project_repo.create_project(values={
        "title": "Project Alpha",
        "description": "This is a description for Project Alpha",
        "owner_id": initial_data["new_user"].user_id,
        "start_date": datetime.utcnow(),
        "deadline": datetime(2024, 12, 31),
        "status_id": initial_data["statuses"]["task_open"].id,
        "priority_id": initial_data["priorities"]["high"].id
    })

    # Создание нового отчёта для проекта
    new_report = await report_repo.create_report(values={
        "title": "First Report",
        "content": "This is the content of the first report",
        "project_id": project.project_id,
        "created_at": datetime.utcnow()
    })
    print(f"Created Report: {new_report}")

    # Получение данных об отчёте без связанных данных
    report_simple = await report_repo.get_report_by_id(new_report.report_id)
    print(f"Report without relations: {report_simple}")

    # Получение данных об отчёте со всеми связями (например проект)
    report_with_relations = await report_repo.get_report_with_relations(new_report.report_id)
    print(f"Report with relations: {report_with_relations}")


async def run_all_tests():
    # 1. Создание всех таблиц
    await create_tables()

    # 2. Вставка начальных данных, которые будут использоваться во всех тестах
    initial_data = await insert_initial_data()

    # 3. Запуск всех тестов
    await test_access()
    await test_user_repo(initial_data)
    await test_status_repo()
    await test_priority_repo()
    await test_notification_repo(initial_data)
    await test_message_repo(initial_data)
    await test_chat_repo(initial_data)
    await test_project_repo(initial_data)
    await test_task_repo(initial_data)
    await test_project_assigned_repo(initial_data)
    await test_task_assigned_repo(initial_data)
    await test_report_repo(initial_data)


# Основной запуск
if __name__ == "__main__":
    asyncio.run(run_all_tests())
