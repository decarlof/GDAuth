=====
Usage
=====

GDAuth creates and shares folders in a Collection. It also creates download links to file and folders listed in the Collection.

For help::

    (globus) $ gdauth -h
    usage: gdauth [-h] [--config FILE]  ...

    options:
      -h, --help     show this help message and exit
      --config FILE  File name of configuration

    Commands:
      
        init         Create configuration file
        select       Select a Collection on the Globus server
        create       Create a folder in the Collection
        share        Share a Collection folder with a user email address
        links        Create download links for all items (folder and files) listed in a Collection folder


To initlialize GDAuth status::

    (globus) $ gdauth init
    2024-03-29 20:18:31,165 - General
    2024-03-29 20:18:31,165 -   config           /Users/decarlo/GDAuth.conf
    2024-03-29 20:18:31,165 -   verbose          True

this creates the GDAuth config file: ~/GDAuth.conf with default values.

To select the Collection you want to create/share folder in:

::

    (globus) $ gdauth select   
    2024-07-21 20:20:20,479 - wget token: AgprNBXnpznQ509OnQgN1mmzyql0DEEkBvgBqe8wjJlq7BG92FvCa7Obpw0owrWgB1d2qmJg9eDDvfymawXzTWwWva
    2024-07-21 20:20:20,479 - Globus access token will expire in 47.98 hours
    2024-07-21 20:20:21,277 - Show all endpoints shared and owned by my globus user credentials
    2024-07-21 20:20:21,277 - *** Endpoints owned with me:
    2024-07-21 20:20:21,277 - *** *** 'handyn' d8e73490-41e8-11ef-963f-453c3ae125a5
    2024-07-21 20:20:21,277 - *** Endpoints shared with me:
    2024-07-21 20:20:21,277 - *** *** '2022-02 Salcedo' 17317f8e-edfb-40bc-bb46-dc0fd759c3e4
    2024-07-21 20:20:21,277 - *** *** '2-BM tomography data' 635c3ecb-f073-42ef-8278-471ed99bfd6e
    2024-07-21 20:20:21,277 - *** *** 'BNL' e909d1d5-b8d9-490a-b9e9-a2ac312bb6fd
    2024-07-21 20:20:21,277 - *** *** 'DARPA scratch' b07f6a40-672c-4ae8-b420-83eb6e925381
    2024-07-21 20:20:21,277 - *** *** 'GitHub share' 9b0090f4-1d23-44da-a45b-2cf93011b477
    2024-07-21 20:20:21,277 - *** *** 'NOCTURN' 4c7b6f7f-240c-4d23-b79f-3b090fc30013
    2024-07-21 20:20:21,277 - *** *** 'NSLS-II data' bedcc818-f3b9-4cba-8d11-8c017f20f5e7
    2024-07-21 20:20:21,277 - *** *** 'Stu-2024-01-recs' a62df544-26df-4f19-8342-cb4fb3baf8f3
    2024-07-21 20:20:21,277 - *** *** 'Test Collection' e55dfefc-2c86-11ee-8806-056a4e394379
    2024-07-21 20:20:21,277 - *** *** 'TomoBank Upload' 42c88e95-a510-415f-8c78-86e23a905e09
    2024-07-21 20:20:21,277 - *** Endpoints shared by me:
    2024-07-21 20:20:21,277 - *** *** '2-BM tomography data' 635c3ecb-f073-42ef-8278-471ed99bfd6e
    2024-07-21 20:20:21,277 - *** *** 'Allen institute data' 144ef39b-65d9-4623-9d5d-7394499261a3
    2024-07-21 20:20:21,277 - *** *** 'BNL' e909d1d5-b8d9-490a-b9e9-a2ac312bb6fd
    2024-07-21 20:20:21,277 - *** *** 'Brain_data' f06b4fc5-6967-4946-8714-740095c262b5
    2024-07-21 20:20:21,278 - *** *** 'Brain_data_bobby' 40deb3f5-2c4c-440c-9bb8-08fb1480dbf9
    2024-07-21 20:20:21,278 - *** *** 'Brain Lamino' 1725e094-d590-4ddc-bd41-1598ca606b87
    2024-07-21 20:20:21,278 - *** *** 'Brain_reconstructions' 021df1ca-b85d-4bf7-8206-00ac2a25a1d0
    2024-07-21 20:20:21,278 - *** *** 'DARPA scratch' b07f6a40-672c-4ae8-b420-83eb6e925381
    2024-07-21 20:20:21,278 - Active: 'ESRF_upload' 7dbacba1-1950-4ab6-b542-127b55ab1428
    2024-07-21 20:20:21,278 - *** *** 'GitHub share' 9b0090f4-1d23-44da-a45b-2cf93011b477
    2024-07-21 20:20:21,278 - *** *** 'IMG share' 401f7b59-7823-4506-82a6-284a34026f0e
    2024-07-21 20:20:21,278 - *** *** 'max iv' d6957027-53ca-4bd4-a61d-3657bbc7bc8d
    2024-07-21 20:20:21,278 - *** *** 'MINT' 54aea3fa-962a-4410-9d7b-8cef7e36916c
    2024-07-21 20:20:21,278 - *** *** 'neuroglancer' b0d438a0-17a1-4ec3-acc0-141327c0523e
    2024-07-21 20:20:21,278 - *** *** 'Nexus Tomo Files' a9f4eab8-9519-4427-bd09-5fc97b380910
    2024-07-21 20:20:21,278 - *** *** 'NOCTURN' 4c7b6f7f-240c-4d23-b79f-3b090fc30013
    2024-07-21 20:20:21,278 - *** *** 'NSLS-II data' bedcc818-f3b9-4cba-8d11-8c017f20f5e7
    2024-07-21 20:20:21,278 - *** *** 'petrel_backup_on_eagle' 07539856-6d69-4234-8c20-d4d996f87ba3
    2024-07-21 20:20:21,278 - *** *** 'Stu-2024-01-recs' a62df544-26df-4f19-8342-cb4fb3baf8f3
    2024-07-21 20:20:21,278 - *** *** 'TomoBank' 9f00a780-4aee-42a7-b7f4-6a2773c8da30
    2024-07-21 20:20:21,278 - *** *** 'TomoBank Upload' 42c88e95-a510-415f-8c78-86e23a905e09
    Do you want to select a different collection ? (Y/N): 
    2024-07-21 20:20:21,278 - 0: 2-BM tomography data: 635c3ecb-f073-42ef-8278-471ed99bfd6e
    2024-07-21 20:20:21,278 - 1: Allen institute data: 144ef39b-65d9-4623-9d5d-7394499261a3
    2024-07-21 20:20:21,278 - 2: BNL: e909d1d5-b8d9-490a-b9e9-a2ac312bb6fd
    2024-07-21 20:20:21,278 - 3: Brain_data: f06b4fc5-6967-4946-8714-740095c262b5
    2024-07-21 20:20:21,278 - 4: Brain_data_bobby: 40deb3f5-2c4c-440c-9bb8-08fb1480dbf9
    2024-07-21 20:20:21,278 - 5: Brain Lamino: 1725e094-d590-4ddc-bd41-1598ca606b87
    2024-07-21 20:20:21,278 - 6: Brain_reconstructions: 021df1ca-b85d-4bf7-8206-00ac2a25a1d0
    2024-07-21 20:20:21,278 - 7: DARPA scratch: b07f6a40-672c-4ae8-b420-83eb6e925381
    2024-07-21 20:20:21,278 - 8: ESRF_upload: 7dbacba1-1950-4ab6-b542-127b55ab1428
    2024-07-21 20:20:21,278 - 9: GitHub share: 9b0090f4-1d23-44da-a45b-2cf93011b477
    2024-07-21 20:20:21,278 - 10: IMG share: 401f7b59-7823-4506-82a6-284a34026f0e
    2024-07-21 20:20:21,278 - 11: max iv: d6957027-53ca-4bd4-a61d-3657bbc7bc8d
    2024-07-21 20:20:21,278 - 12: MINT: 54aea3fa-962a-4410-9d7b-8cef7e36916c
    2024-07-21 20:20:21,279 - 13: neuroglancer: b0d438a0-17a1-4ec3-acc0-141327c0523e
    2024-07-21 20:20:21,279 - 14: Nexus Tomo Files: a9f4eab8-9519-4427-bd09-5fc97b380910
    2024-07-21 20:20:21,279 - 15: NOCTURN: 4c7b6f7f-240c-4d23-b79f-3b090fc30013
    2024-07-21 20:20:21,279 - 16: NSLS-II data: bedcc818-f3b9-4cba-8d11-8c017f20f5e7
    2024-07-21 20:20:21,279 - 17: petrel_backup_on_eagle: 07539856-6d69-4234-8c20-d4d996f87ba3
    2024-07-21 20:20:21,279 - 18: Stu-2024-01-recs: a62df544-26df-4f19-8342-cb4fb3baf8f3
    2024-07-21 20:20:21,279 - 19: TomoBank: 9f00a780-4aee-42a7-b7f4-6a2773c8da30
    2024-07-21 20:20:21,279 - 20: TomoBank Upload: 42c88e95-a510-415f-8c78-86e23a905e09
    2024-07-21 20:20:21,279 - Select one by entering its index:
    Please select an index: 7
    2024-07-21 20:20:30,899 - You selected index 7: DARPA scratch: b07f6a40-672c-4ae8-b420-83eb6e925381
    2024-07-21 20:24:44,247 - A new token will be generated next time you run GDAuth
    2024-07-21 20:24:44,247 - General
    2024-07-21 20:24:44,247 -   config           /Users/decarlo/gdauth.conf
    2024-07-21 20:24:44,247 -   verbose          True
    2024-07-21 20:24:44,247 - Globus
    2024-07-21 20:24:44,247 -   app_uuid         2f1fd715-ee09-43f9-9b48-1f06810bcc70
    2024-07-21 20:24:44,247 -   ep_uuid          401f7b59-7823-4506-82a6-284a34026f0e


